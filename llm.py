import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi_poe import (
    ProtocolMessage,
    QueryRequest,
    get_final_response,
    upload_file_sync,
)
from fastapi_poe.client import PROTOCOL_VERSION

load_dotenv()

TEMPERATURE = 0

API_KEY = os.environ.get("POE_API_KEY", "")
if not API_KEY:
    raise ValueError("Could not find POE_API_KEY variable in the environment")


class LLM:
    user_id: str = str(uuid4())

    async def get_response(
        self,
        model: str,
        query: str,
        doc_urls: list[str] = [],
        system_prompt: str | None = None,
    ) -> str:
        attachments = []
        for doc_url in doc_urls:
            attachment = upload_file_sync(open(doc_url, "rb"), api_key=API_KEY)
            attachments.append(attachment)

        messages = []
        if system_prompt:
            messages.append(ProtocolMessage(role="system", content=system_prompt))
        messages.append(
            ProtocolMessage(role="user", content=query, attachments=attachments)
        )

        request = QueryRequest(
            version=PROTOCOL_VERSION,
            type="query",
            query=messages,
            user_id=self.user_id,
            conversation_id="",
            message_id="",
            api_key=API_KEY,
            temperature=TEMPERATURE,
        )
        response = await get_final_response(
            request=request, bot_name=model, api_key=API_KEY
        )
        return response


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
            query="Translate this document into Spanish",
            doc_urls=["./txt/sample.txt"],
            system_prompt="You are a helpful assistant. Answer user queries succintly.",
        )
        print("\nAnswer: " + answer)

    asyncio.run(main())
