from pathlib import Path
from typing import Any

import pdfplumber
from langchain.docstore.document import Document
from langchain.retrievers import EnsembleRetriever
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_FOLDER = "chroma_db"

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def page_number(doc: Document) -> int:
    return doc.metadata["page_number"]


class Retriever:
    vector_store: Chroma
    filename: str
    bm25_retriever: BM25Retriever

    def __init__(self, pdf_doc_url: str):
        # Init vector store
        self.vector_store = Chroma(
            collection_name="docs",
            persist_directory=CHROMA_FOLDER,
            embedding_function=embedding,
        )

        # Load document
        self.filename = Path(pdf_doc_url).stem
        print(f"Loading document {self.filename}...")
        with pdfplumber.open(pdf_doc_url) as pdf:
            # Chunk by pages
            for idx, page in enumerate(pdf.pages):
                text = page.extract_text(layout=True)
                doc = Document(
                    page_content=text.strip(),
                    metadata={"filename": self.filename, "page_number": idx + 1},
                )

            # Create BM25 retriever
            self.bm25_retriever = BM25Retriever.from_documents([doc])

            # Add documents to vector store, if needed
            if not self._has_doc(doc):
                self.vector_store.add_documents([doc])

    def get_ensemble_retriever(self, k: int) -> EnsembleRetriever:
        self.bm25_retriever.k = k
        semantic_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": k, "filter": {"filename": self.filename}}
        )
        return EnsembleRetriever(
            retrievers=[self.bm25_retriever, semantic_retriever], weights=[0.5, 0.5]
        )

    def _has_doc(self, doc: Document) -> bool:
        filename = doc.metadata["filename"]
        match = self.vector_store.get(where={"filename": filename})
        has_doc = len(match["ids"]) > 0
        return has_doc

    def get_relevant_documents(self, query: str, k: int) -> dict[str, Any]:
        print("Getting relevant documents...")
        docs = self.get_ensemble_retriever(k=k).invoke(query)

        return {
            "filename": self.filename,
            "pages": [
                {
                    "page_number": d.metadata["page_number"],
                    "text": d.page_content,
                }
                for d in sorted(docs, key=page_number)
            ],
        }


if __name__ == "__main__":
    retriever = Retriever(pdf_doc_url="./pdf/Apple_SEC_filing_2024.pdf")
    query = "How many employees does Apple have?"
    result = retriever.get_relevant_documents(query=query, k=10)
    for page in result["pages"]:
        print(f"Page {page['page_number']}:\n{page['text']}")
