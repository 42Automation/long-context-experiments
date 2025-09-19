from math import floor
from pathlib import Path

from utils import get_filler_content, get_num_tokens

MAX_CONTEXT_WINDOW = 256_000
CONTEXT_WINDOW_BUFFER_PERCENT = 5
MAX_EFFECTIVE_CONTEXT_WINDOW = MAX_CONTEXT_WINDOW - floor(
    MAX_CONTEXT_WINDOW * CONTEXT_WINDOW_BUFFER_PERCENT / 100
)


def _has_default_treatment(experiment: dict) -> bool:
    if (treatments := experiment.get("treatments")) is not None:
        if "default" not in treatments:
            return False
    return True


def get_pdf_urls(experiment: dict) -> list[str]:
    doc_urls = (
        experiment.get("reference_doc_urls", [])
        if _has_default_treatment(experiment)
        else []
    )
    return [d for d in doc_urls if Path(d).suffix == ".pdf"]


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


def get_texts(
    experiment: dict, max_context: int = MAX_EFFECTIVE_CONTEXT_WINDOW
) -> list[str]:
    if _has_default_treatment(experiment):
        return _get_default_texts(experiment, max_context)

    return []
