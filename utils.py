from tiktoken import get_encoding

tokenizer_encoding = get_encoding(
    "cl100k_base"
)  # Use base tokenizer encoding as approximation


def is_anthropic_model(model: str) -> bool:
    return "claude" in model.lower()


def get_num_tokens(text: str) -> int:
    return len(tokenizer_encoding.encode(text))


def get_filler_content(
    filler_doc_urls: list[str], current_context: int, max_context: int
) -> str:
    """
    Build filler text from *filler_doc_urls* given the number of tokens that are
    already used (*current_context*).

    The function computes the remaining token budget as:
        ``remaining = max_context - current_context``

    It then reads the filler documents line-by-line (plain-text) and stops
    once the accumulated token count reaches this remaining budget.  Token
    counting uses ``get_num_tokens``.
    """
    print(
        f"Getting filler content with current context {current_context} tokens (max {max_context})"
    )
    # Compute how many tokens we can still add
    remaining_context = max_context - current_context
    if remaining_context <= 0:
        return ""

    token_budget = remaining_context  # alias for clarity

    filler_parts: list[str] = []
    tokens_used = 0

    for doc_url in filler_doc_urls:
        if tokens_used >= token_budget:
            break

        try:
            with open(doc_url, "r", encoding="utf-8") as f:
                for line in f:
                    clean_line = line.rstrip("\n")
                    line_tokens = get_num_tokens(clean_line)

                    if tokens_used + line_tokens > token_budget:
                        break

                    filler_parts.append(clean_line)
                    tokens_used += line_tokens
        except FileNotFoundError:
            continue
    return "\n".join(filler_parts)
