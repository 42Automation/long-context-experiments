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


def get_sorted_docs(filename: str, docs: list[Document]) -> list[Document]:
    filtered = filter(lambda d: d.metadata["filename"] == filename, docs)
    return sorted(filtered, key=page_number)


class Retriever:
    vector_store: Chroma

    def __init__(self):
        self.vector_store = Chroma(
            collection_name="docs",
            persist_directory=CHROMA_FOLDER,
            embedding_function=embedding,
        )

    def _has_doc(self, doc: Document) -> bool:
        filename = doc.metadata["filename"]
        match = self.vector_store.get(where={"filename": filename})
        has_doc = len(match["ids"]) > 0
        return has_doc

    def _get_retriever(self, pdf_doc_urls: list[str], k: int) -> EnsembleRetriever:
        # Load documents
        source_docs = []
        for doc_url in pdf_doc_urls:
            with pdfplumber.open(doc_url) as pdf:
                # Chunk by pages
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text(layout=True)
                    filename = Path(doc_url).stem
                    source_docs.append(
                        Document(
                            page_content=text.strip(),
                            metadata={"filename": filename, "page_number": idx + 1},
                        )
                    )

        # Create BM25 retriever
        bm25_retriever = BM25Retriever.from_documents(source_docs)
        bm25_retriever.k = k

        # Add documents to vector store, if needed
        new_docs = [d for d in source_docs if (not self._has_doc(d)) and d.page_content]
        if new_docs:
            self.vector_store.add_documents(new_docs)

        semantic_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": k, "filter": {"filename": filename}}
        )

        return EnsembleRetriever(
            retrievers=[bm25_retriever, semantic_retriever], weights=[0.5, 0.5]
        )

    def get_relevant_documents(
        self, query: str, pdf_doc_urls: list[str], k: int
    ) -> list[dict[str, Any]]:
        print("Getting retriever...")
        retriever = self._get_retriever(pdf_doc_urls, k)

        names = [Path(f).stem for f in pdf_doc_urls]

        print("Getting relevant documents...")
        docs = retriever.invoke(query)

        sorted_docs = []
        for name in names:
            sorted_docs.append(
                {
                    "filename": name,
                    "pages": [
                        {
                            "page_number": d.metadata["page_number"],
                            "text": d.page_content,
                        }
                        for d in get_sorted_docs(name, docs)
                    ],
                }
            )
        return sorted_docs


if __name__ == "__main__":
    doc_urls = ["./pdf/Apple_SEC_filing_2024.pdf"]
    retriever = Retriever()
    query = "How many employees does Apple have?"
    docs = retriever.get_relevant_documents(query, doc_urls, 10)

    for doc in docs:
        print(f"Filename: {doc['filename']}")
        pages = doc["pages"]
        for page in pages:
            print(f"Page {page['page_number']}:\n{page['text']}")
