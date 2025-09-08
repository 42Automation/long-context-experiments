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
    ) -> str:
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

        print(f"response: {response}")

        return response.choices[0].message.content


if __name__ == "__main__":
    import asyncio

    async def main():
        llm = LLM()
        answer = await llm.get_response(
            model="GPT-5", query="Tell me about you in 2 lines"
        )
        print("\nAnswer: " + answer)

        answer = await llm.get_response(
            model="Qwen-2.5-7B-T",
            query="Tell me about you in 2 lines",
            system_prompt="You are a helpful assistant talking in English pirate",
        )
        print("\nAnswer: " + answer)

        answer = await llm.get_response(
            model="Gemini-2.5-Flash-Lite",
            query="What kind of document is this? --thinking_budget 0 --web_search false",
            doc_urls=["./pdf/Apple_segment_operating_performance.pdf"],
            system_prompt="You are a helpful assistant. Answer user queries succintly.",
        )
        print("\nAnswer: " + answer)

        answer = await llm.get_response(
            model="Gemini-2.5-Flash-Lite",
            query="Translate this document into Spanish --thinking_budget 0 --web_search false",
            doc_urls=["./txt/sample.txt"],
            system_prompt="You are a helpful assistant. Answer user queries succintly.",
        )
        print("\nAnswer: " + answer)

        answer = await llm.get_response(
            model="GPT-5-mini",
            query="What do these 2 documents have in common?",
            doc_urls=[
                "./txt/sample.txt",
                "./pdf/Apple_segment_operating_performance.pdf",
            ],
            system_prompt="You are a helpful assistant. Answer user queries succintly.",
        )
        print("\nAnswer: " + answer)

    asyncio.run(main())
