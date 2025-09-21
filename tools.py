from smolagents import Tool

from rag import Retriever
from utils import get_pages_text


class RetrieverTool(Tool):
    name = "lexical_and_semantic_retriever"
    description = "Retriever tool to fetch relevant excertps from the reference documents related to a given query."
    inputs = {
        "query": {
            "description": "A query, to be answered based on the relevant data found in the reference documents",
            "type": "string",
        },
        "k": {
            "description": """"Base to calculate the number of document excerpts to return.
The retrieval generally etches 2*k excerpts of information for each of the reference documents.
""",
            "type": "integer",
        },
    }
    output_type = "array"

    retriever: Retriever

    def forward(self, query: str, k: int) -> list[str]:
        if not self.retriever:
            raise ValueError(
                "Tool was not initialized. Can't find retriever dependency."
            )
        docs = self.retriever.get_relevant_documents(query=query, k=k)
        texts = []
        for doc in docs:
            pages_text = get_pages_text(pages=doc["pages"], filename=doc["filename"])
            texts.append(pages_text)
        return texts
