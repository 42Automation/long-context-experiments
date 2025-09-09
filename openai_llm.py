import os
from base64 import b64encode
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from prompts import SYSTEM_PROMPT

load_dotenv()

TEMPERATURE = 0

API_KEY = os.environ.get("POE_API_KEY", "")
if not API_KEY:
    raise ValueError("Could not find POE_API_KEY variable in the environment")
BASE_URL = os.environ.get("POE_BASE_URL", "")
if not BASE_URL:
    raise ValueError("Could not find POE_BASE_URL variable in the environment")

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)


class LLM:
    async def get_response(
        self,
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
        response = await client.chat.completions.create(
            model=model, temperature=TEMPERATURE, messages=messages
        )

        return {"text": response.choices[0].message.content, "usage": response.usage}


if __name__ == "__main__":
    import asyncio

    llm = LLM()

    async def run_experiment(
        description: str,
        model: str,
        query: str,
        doc_urls: list[str] = [],
        system_prompt: str = SYSTEM_PROMPT,
    ):
        answer = await llm.get_response(
            model=model, query=query, doc_urls=doc_urls, system_prompt=system_prompt
        )
        tokens = answer["usage"].prompt_tokens
        print(f"{description} ({tokens} input tokens) [{model}]: {answer['text']}\n")

    async def main():
        functional_tasks = [
            run_experiment(
                description="Simple query",
                model="Claude-Sonnet-3.7",
                query="Tell me about you in 2 lines --thinking_budget 0",
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
                model="Grok-3",
                query="What is the filing date for the fifth amended and restated investors'rights agreement?",
                doc_urls=[
                    "./pdf/Tesla_exhibit_schedules.pdf",
                ],
            ),
            run_experiment(
                description="Answer over TXT file",
                model="Grok-3",
                query="What is the filing date for the fifth amended and restated investors'rights agreement?",
                doc_urls=[
                    "./txt/Tesla_exhibit_schedules.txt",
                ],
            ),
            run_experiment(
                description="Answer over MD file",
                model="Grok-3",
                query="What is the filing date for the fifth amended and restated investors'rights agreement?",
                doc_urls=[
                    "./md/Tesla_exhibit_schedules.md",
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
