import os
from base64 import b64encode
from pathlib import Path

from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from openai import AsyncOpenAI

from models import MODEL_IDS
from prompts import SYSTEM_PROMPT

load_dotenv()

TEMPERATURE = 0

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
anthropic_cient = AsyncAnthropic()


def _is_anthropic_model(model: str) -> bool:
    return "claude" in model.lower()


async def _get_response_with_poe_client(
    model: str,
    query: str,
    doc_urls: list[str] = [],
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    # Get file data
    content = []
    for doc_url in doc_urls:
        with open(doc_url, "rb") as doc:
            print(f"Getting data from {Path(doc_url).name}")
            extension = Path(doc_url).suffix
            if extension == ".pdf":
                doc_content = b64encode(doc.read()).decode("utf-8")
                doc_message = {
                    "type": "file",
                    "file": {
                        "filename": Path(doc_url).name,
                        "file_data": f"data:application/pdf;base64,{doc_content}",
                    },
                }
            else:
                doc_content = doc.read().decode("utf-8")
                doc_message = {"type": "text", "text": doc_content}

            content.append(doc_message)

    content.append({"type": "text", "text": query})

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": content})

    # Get response
    model_id = MODEL_IDS[model]
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
    doc_urls: list[str] = [],
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    # Get file data
    content = []
    for doc_url in doc_urls:
        with open(doc_url, "rb") as doc:
            print(f"Getting data from {Path(doc_url).name}")
            extension = Path(doc_url).suffix
            if extension == ".pdf":
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
            else:
                doc_content = doc.read().decode("utf-8")
                content.append({"type": "text", "text": doc_content})

    content.append({"type": "text", "text": query})

    # Build messages
    messages = [{"role": "user", "content": content}]

    # Get response
    model_id = MODEL_IDS[model]
    response = await anthropic_cient.messages.create(
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
    doc_urls: list[str] = [],
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    if _is_anthropic_model(model):
        print("Using ANTHROPIC client")
        return await _get_response_with_anthropic_client(
            model, query, doc_urls, system_prompt
        )

    print("Using POE client")
    return await _get_response_with_poe_client(model, query, doc_urls, system_prompt)


if __name__ == "__main__":
    import asyncio

    async def run_experiment(
        description: str,
        model: str,
        query: str,
        doc_urls: list[str] = [],
        system_prompt: str = SYSTEM_PROMPT,
    ):
        answer = await get_response(
            model=model, query=query, doc_urls=doc_urls, system_prompt=system_prompt
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
                doc_urls=["./pdf/Apple_segment_operating_performance.pdf"],
            ),
            run_experiment(
                description="Answer over TXT file",
                model="Grok-3",
                query="Translate this document into Spanish",
                doc_urls=["./txt/Apple_segment_operating_performance.txt"],
            ),
            run_experiment(
                description="Answer over multiple files",
                model="GPT-5-mini",
                query="What companies are featured in the provided documents? --reasoning_effort minimal",
                doc_urls=[
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
                doc_urls=[
                    "./pdf/Tesla_exhibit_schedules.pdf",
                ],
            ),
            run_experiment(
                description="Answer over TXT file",
                model="Claude-Sonnet-3.7",
                query="What is the filing date for the fifth amended and restated investors'rights agreement?",
                doc_urls=[
                    "./txt/Tesla_exhibit_schedules.txt",
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
