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
    filenames: list[str]
    bm25_per_doc: dict[str, BM25Retriever]

    def __init__(self, pdf_doc_urls: list[str]):
        # Init vector store
        self.vector_store = Chroma(
            collection_name="docs",
            persist_directory=CHROMA_FOLDER,
            embedding_function=embedding,
        )

        # Load documents
        source_docs = []
        self.filenames = []
        for doc_url in pdf_doc_urls:
            filename = Path(doc_url).stem
            print(f"Loading {filename}...")
            self.filenames.append(filename)
            with pdfplumber.open(doc_url) as pdf:
                # Chunk by pages
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text(layout=True)
                    source_docs.append(
                        Document(
                            page_content=text.strip(),
                            metadata={"filename": filename, "page_number": idx + 1},
                        )
                    )

        # Create BM25 retrievers
        self.bm25_per_doc: dict[str, BM25Retriever] = {}
        for filename in self.filenames:
            docs_for_file = [
                d for d in source_docs if d.metadata["filename"] == filename
            ]
            b = BM25Retriever.from_documents(docs_for_file)
            self.bm25_per_doc[filename] = b

        # Add documents to vector store, if needed
        new_docs = [d for d in source_docs if (not self._has_doc(d)) and d.page_content]
        if new_docs:
            print(
                f"Adding following document(s) to vector store: {', '.join(set([d.metadata['filename'] for d in new_docs]))}"
            )
            self.vector_store.add_documents(new_docs)

    def _get_retriever(self, filename: str, k: int) -> EnsembleRetriever:
        assert filename in list(self.bm25_per_doc.keys())
        bm25_retriever = self.bm25_per_doc[filename]
        bm25_retriever.k = k

        semantic_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": k, "filter": {"filename": filename}}
        )

        return EnsembleRetriever(
            retrievers=[bm25_retriever, semantic_retriever], weights=[0.5, 0.5]
        )

    def _has_doc(self, doc: Document) -> bool:
        filename = doc.metadata["filename"]
        match = self.vector_store.get(where={"filename": filename})
        has_doc = len(match["ids"]) > 0
        return has_doc

    def get_relevant_documents(self, query: str, k: int) -> list[dict[str, Any]]:
        print("Getting relevant documents...")
        docs = []
        for filename in self.filenames:
            retriever = self._get_retriever(filename=filename, k=k)
            matches = retriever.invoke(query)
            docs.append(
                {
                    "filename": filename,
                    "pages": [
                        {
                            "page_number": d.metadata["page_number"],
                            "text": d.page_content,
                        }
                        for d in get_sorted_docs(filename, matches)
                    ],
                }
            )
        return docs


if __name__ == "__main__":
    pdf_doc_urls = [
        "./pdf/Apple_SEC_filing_2024.pdf",
        "./pdf/Tesla_SEC_filing_2024.pdf",
    ]
    retriever = Retriever(pdf_doc_urls=pdf_doc_urls)
    query = "How many employees does the company have?"
    docs = retriever.get_relevant_documents(query=query, k=10)

    for doc in docs:
        pages = doc["pages"]
        print(f"\nFilename: {doc['filename']} -- {len(pages)} excerpts")
        print("-------------------------")
        for page in pages:
            print(f"Page {page['page_number']}:\n{page['text'][:100]}")
