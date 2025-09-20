from math import floor
from pathlib import Path

from rag import Retriever
from utils import get_filler_content, get_num_tokens, get_pages_text

MAX_CONTEXT_WINDOW = 256_000
CONTEXT_WINDOW_BUFFER_PERCENT = 5
MAX_EFFECTIVE_CONTEXT_WINDOW = MAX_CONTEXT_WINDOW - floor(
    MAX_CONTEXT_WINDOW * CONTEXT_WINDOW_BUFFER_PERCENT / 100
)


def _has_default_treatment(experiment: dict) -> bool:
    if (treatments := experiment.get("treatments")) is not None:
        if "default" not in list(treatments.keys()):
            return False
    return True


def _has_rag_treatment(experiment: dict) -> bool:
    return "rag" in list(experiment.get("treatments", {}).keys())


def _has_agent_treatment(experiment: dict) -> bool:
    return "agent" in list(experiment.get("treatments", {}).keys())


def _get_default_texts(experiment: dict, max_context: int) -> list[str]:
    texts = []

    # Get reference docs, if present
    for text_doc_url in experiment.get("reference_doc_urls", []):
        if Path(text_doc_url).suffix in [".txt", ".md"]:
            with open(text_doc_url, "r", encoding="utf-8") as f:
                text = f.read()
                texts.append(text)

    # Add filler text, if needed
    query = experiment.get("query", "")
    current_context_size = sum(get_num_tokens(t) for t in texts)
    filler_doc_urls = experiment.get("filler_doc_urls", [])
    if filler_doc_urls:
        filler_content = get_filler_content(
            filler_doc_urls=filler_doc_urls,
            current_context=current_context_size + get_num_tokens(query),
            max_context=max_context,
        )
        if filler_content:
            texts.append(text)

    return texts


def _get_rag_texts(experiment: dict, dump_texts: bool = True) -> list[str]:
    if (query := experiment.get("query")) is None:
        return []

    experiment_id = experiment["id"]
    k = experiment.get("treatments", {}).get("rag", {}).get("k", 5)
    pdf_doc_urls = [
        d for d in experiment.get("reference_doc_urls", []) if Path(d).suffix == ".pdf"
    ]

    retriever = Retriever(pdf_doc_urls=pdf_doc_urls)
    docs = retriever.get_relevant_documents(query, k=k)

    texts = []
    for doc in docs:
        filename = doc["filename"]
        full_text = get_pages_text(pages=doc["pages"], filename=filename)
        if dump_texts:
            with open(f"./rag_texts/{experiment_id}_{filename}.txt", "w") as f:
                f.write(full_text)
        texts.append(full_text)
    return texts


def get_pdf_urls(experiment: dict) -> list[str]:
    if _has_default_treatment(experiment):
        return [
            d
            for d in experiment.get("reference_doc_urls", [])
            if Path(d).suffix == ".pdf"
        ]
    return []


def get_texts(
    experiment: dict, max_context: int = MAX_EFFECTIVE_CONTEXT_WINDOW
) -> list[str]:
    if _has_default_treatment(experiment):
        return _get_default_texts(experiment, max_context)

    if _has_rag_treatment(experiment):
        return _get_rag_texts(experiment)

    return []
