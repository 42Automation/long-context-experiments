from smolagents import Tool

from rag import Retriever
from utils import get_pages_text


class RetrieverTool(Retriever, Tool):
    name = "lexical_and_semantic_retriever"
    description = "You cannot load documents yourself: instead call this retriever to fetch relevant excertps from the reference documents related to the query"
    inputs = {
        "query": {
            "description": "A user query, to be answered based on the relevant data foud in the reference documents",
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

    def forward(self, query: str, k: int) -> list[str]:
        docs = self.get_relevant_documents(query=query, k=k)
        texts = []
        for doc in docs:
            pages_text = get_pages_text(pages=docs["pages"], filename=docs["filename"])
            texts.append(pages_text)
        return texts
