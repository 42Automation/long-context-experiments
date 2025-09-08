import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TEMPERATURE = 0

API_KEY = os.environ.get("POE_API_KEY", "")
if not API_KEY:
    raise ValueError("Could not find POE_API_KEY variable in the environment")
BASE_URL = os.environ.get("POE_BASE_URL", "")
if not BASE_URL:
    raise ValueError("Could not find POE_BASE_URL variable in the environment")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


class LLM:
    async def get_response(
        self,
        model: str,
        query: str,
        doc_urls: list[str] = [],
        system_prompt: str | None = None,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        # attachments = []
        # for doc_url in doc_urls:
        #     attachment = upload_file_sync(open(doc_url, "rb"), api_key=API_KEY)
        #     attachments.append(attachment)

        response = client.chat.completions.create(
            model=model, messages=messages, temperature=TEMPERATURE
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

        # answer = await llm.get_response(
        #     model="Qwen-2.5-7B-T",
        #     query="Tell me about you in 2 lines",
        #     system_prompt="You are a helpful assistant talking in English pirate",
        # )
        # print("\nAnswer: " + answer)

        # answer = await llm.get_response(
        #     model="Gemini-2.5-Flash-Lite",
        #     query="Translate this document into Spanish",
        #     doc_urls=["./txt/sample.txt"],
        #     system_prompt="You are a helpful assistant. Answer user queries succintly.",
        # )
        # print("\nAnswer: " + answer)

    asyncio.run(main())
