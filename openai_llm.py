import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

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
        system_prompt: str | None = None,
    ) -> str:
        with open(doc_urls[0], "rb") as doc:
            base64_pdf = base64.b64encode(doc.read()).decode("utf-8")

        response = await client.chat.completions.create(
            model=model,
            temperature=TEMPERATURE,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "file",
                            "file": {
                                "filename": Path(doc_urls[0]).name,
                                "file_data": f"data:application/pdf;base64,{base64_pdf}",
                            },
                        },
                        {
                            "type": "text",
                            "text": query,
                        },
                    ],
                },
            ],
        )

        print(f"response: {response}")

        return response.choices[0].message.content


if __name__ == "__main__":
    import asyncio

    async def main():
        llm = LLM()
        # answer = await llm.get_response(
        #     model="GPT-5", query="Tell me about you in 2 lines"
        # )
        # print("\nAnswer: " + answer)

        # answer = await llm.get_response(
        #     model="Qwen-2.5-7B-T",
        #     query="Tell me about you in 2 lines",
        #     system_prompt="You are a helpful assistant talking in English pirate",
        # )
        # print("\nAnswer: " + answer)

        answer = await llm.get_response(
            model="Gemini-2.5-Flash-Lite",
            query="What kind of document is this?",
            doc_urls=["./pdf/Apple_segment_operating_performance.pdf"],
            system_prompt="You are a helpful assistant. Answer user queries succintly.",
        )
        print("\nAnswer: " + answer)

        # answer = await llm.get_response(
        #     model="Gemini-2.5-Flash-Lite",
        #     query="Translate this document into Spanish",
        #     doc_urls=["./txt/sample.txt"],
        #     system_prompt="You are a helpful assistant. Answer user queries succintly.",
        # )
        # print("\nAnswer: " + answer)

    asyncio.run(main())
