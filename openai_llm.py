import os

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
        attachment_ids = []
        for doc_url in doc_urls:
            with open(doc_url, "rb") as doc:
                upload = await client.files.create(file=doc, purpose="assistants")
                attachment_ids.append(upload.id)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if attachment_ids:
            content = [{"type": "input_text", "text": query}]
            for id in attachment_ids:
                content.append({"type": "file_reference", "file_id": id})
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": query})

        print("Messages")
        print(messages)

        response = await client.responses.create(
            model=model, temperature=TEMPERATURE, input=messages
        )

        print(f"response: {response}")

        return response.output_text


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
            query="Translate this document into Spanish",
            doc_urls=["./txt/sample.txt"],
            system_prompt="You are a helpful assistant. Answer user queries succintly.",
        )
        print("\nAnswer: " + answer)

    asyncio.run(main())
