import os
from base64 import b64encode
from math import floor
from pathlib import Path

from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from openai import AsyncOpenAI

from models import MODEL_IDS
from prompts import SYSTEM_PROMPT
from utils import is_anthropic_model

load_dotenv()

TEMPERATURE = 0
MAX_CONTEXT_WINDOW = 256_000
CONTEXT_WINDOW_BUFFER_PERCENT = 5
MAX_EFFECTIVE_CONTEXT_WINDOW = MAX_CONTEXT_WINDOW - floor(
    MAX_CONTEXT_WINDOW * CONTEXT_WINDOW_BUFFER_PERCENT / 100
)

POE_API_KEY = os.environ.get("POE_API_KEY", "")
if not POE_API_KEY:
    raise ValueError("Could not find POE_API_KEY variable in the environment")
POE_BASE_URL = os.environ.get("POE_BASE_URL", "")
if not POE_BASE_URL:
    raise ValueError("Could not find POE_BASE_URL variable in the environment")
poe_client = AsyncOpenAI(api_key=POE_API_KEY, base_url=POE_BASE_URL)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not ANTHROPIC_API_KEY:
    raise ValueError("Could not find ANTHROPIC_API_KEY variable in the environment")
anthropic_client = AsyncAnthropic()


async def _get_response_with_poe_client(
    model: str,
    query: str,
    pdf_doc_urls: list[str],
    text_docs: list[str],
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    content = []

    # Get pdf files, if any
    for doc_url in pdf_doc_urls:
        with open(doc_url, "rb") as doc:
            print(f"Getting data from {Path(doc_url).name}")
            doc_content = b64encode(doc.read()).decode("utf-8")
            doc_message = {
                "type": "file",
                "file": {
                    "filename": Path(doc_url).name,
                    "file_data": f"data:application/pdf;base64,{doc_content}",
                },
            }
            content.append(doc_message)

    # Get text docs, if any
    for text in text_docs:
        content.append({"type": "text", "text": text})

    # Add query
    content.append({"type": "text", "text": query})

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": content})

    # Get response
    model_id = MODEL_IDS.get(model, model)
    response = await poe_client.chat.completions.create(
        model=model_id, temperature=TEMPERATURE, messages=messages
    )

    return {
        "text": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens,
    }


async def _get_response_with_anthropic_client(
    model: str,
    query: str,
    pdf_doc_urls: list[str],
    text_docs: list[str],
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    content = []

    # Get pdf files, if any
    for doc_url in pdf_doc_urls:
        with open(doc_url, "rb") as doc:
            print(f"Getting data from {Path(doc_url).name}")
            doc_content = b64encode(doc.read()).decode("utf-8")
            doc_message = {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": doc_content,
                },
            }
            content.append(doc_message)

    # Get text docs, if any
    for text in text_docs:
        content.append({"type": "text", "text": text})

    # Add query
    content.append({"type": "text", "text": query})

    # Build messages
    messages = [{"role": "user", "content": content}]

    # Get response
    model_id = MODEL_IDS.get(model, model)
    response = await anthropic_client.messages.create(
        max_tokens=300,
        messages=messages,
        model=model_id,
        temperature=TEMPERATURE,
        system=system_prompt,
    )

    return {
        "text": response.content[-1].text,
        "input_tokens": response.usage.input_tokens,
    }


async def get_response(
    model: str,
    query: str,
    pdf_doc_urls: list[str],
    text_docs: list[str],
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    if is_anthropic_model(model):
        print("Using ANTHROPIC client")
        return await _get_response_with_anthropic_client(
            model, query, pdf_doc_urls, text_docs, system_prompt
        )

    print("Using POE client")
    return await _get_response_with_poe_client(
        model, query, pdf_doc_urls, text_docs, system_prompt
    )


if __name__ == "__main__":
    import asyncio

    def get_text_docs(doc_url: str) -> str:
        with open(doc_url, "r") as f:
            return f.read()

    async def run_experiment(
        description: str,
        model: str,
        query: str,
        pdf_doc_urls: list[str] = [],
        text_docs: list[str] = [],
        system_prompt: str = SYSTEM_PROMPT,
    ):
        answer = await get_response(
            model, query, pdf_doc_urls, text_docs, system_prompt
        )
        print(
            f"{description} ({answer['input_tokens']} input tokens) [{model}]: {answer['text']}\n"
        )

    async def main():
        functional_tasks = [
            run_experiment(
                description="Simple query",
                model="Claude-Sonnet-3.7",
                query="Tell me about you in 2 lines",
                system_prompt="Contesta en español",
            ),
            run_experiment(
                description="Simple query with custom system prompt",
                model="Qwen3-235B-2507-FW",
                query="Tell me about you in 2 lines",
                system_prompt="You are a helpful assistant talking in English pirate",
            ),
            run_experiment(
                description="Answer over PDF file",
                model="Gemini-2.5-Flash-Lite",
                query="What kind of document is this? --thinking_budget 0 --web_search false",
                pdf_doc_urls=["./pdf/Apple_segment_operating_performance.pdf"],
            ),
            run_experiment(
                description="Answer over TXT file",
                model="Grok-3",
                query="Translate this document into Spanish",
                text_docs=[
                    get_text_docs("./txt/Apple_segment_operating_performance.txt")
                ],
            ),
            run_experiment(
                description="Answer over multiple files",
                model="GPT-5-mini",
                query="What companies are featured in the provided documents? --reasoning_effort minimal",
                pdf_doc_urls=[
                    "./pdf/Tesla_exhibit_schedules.pdf",
                    "./pdf/Apple_segment_operating_performance.pdf",
                ],
            ),
        ]

        document_processing_tasks = [
            run_experiment(
                description="Answer over PDF file",
                model="Claude-Sonnet-3.7",
                query="What is the filing date for the fifth amended and restated investors'rights agreement?",
                pdf_doc_urls=[
                    "./pdf/Tesla_exhibit_schedules.pdf",
                ],
            ),
            run_experiment(
                description="Answer over TXT file",
                model="Claude-Sonnet-3.7",
                query="What is the filing date for the fifth amended and restated investors'rights agreement?",
                text_docs=[
                    get_text_docs("./txt/Tesla_exhibit_schedules.txt"),
                ],
            ),
        ]

        tasks = functional_tasks + document_processing_tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"⚠️  Task {idx + 1} raised an exception:")
                print(f"   {type(result).__name__}: {result}")

    asyncio.run(main())
