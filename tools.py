from smolagents import Tool

from rag import Retriever
from utils import get_pages_text


class RetrieverTool(Retriever, Tool):
    name = "lexical_and_semantic_retriever"
    description = "You cannot load documents yourself: instead call this retriever to fetch relevant information to the query from reference documents"
    inputs = {
        "query": {
            "description": "A user query, to be answered based on the relevant data foud in the reference documents",
            "type": "string",
        }
    }
    output_type = "array"

    def forward(self, query: str) -> list[str]:
        docs = self.get_relevant_documents(query=query)
        texts = []
        for doc in docs:
            pages_text = get_pages_text(docs["pages"])
            texts.append(pages_text)
        return texts
