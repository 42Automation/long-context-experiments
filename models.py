PREMIUM_MODELS = [
    "GPT-5",
    "Claude-Sonnet-4",
    "Gemini-2.5-Pro",
    "Grok-4",
    "Qwen3-235B-A22B",
]

STANDARD_MODELS = [
    "GPT-5-mini",
    "Claude-Sonnet-3.7",
    "Gemini-2.5-Flash",
    "Qwen3-235B-2507-FW",
]

MODEL_PARAMS = {
    "Gemini-2.5-Flash": ["--web_search false", "--thinking_budget 0"],
    "GPT-5-mini": ["--reasoning_effort minimal"],
    "Claude-Sonnet-3.7": ["--thinking_budget 0"],
}

SAMPLE_MODELS = ["Gemini-2.5-Flash"]

JUDGE_MODEL = "GPT-5-mini"
