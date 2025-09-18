PREMIUM_MODELS = [
    "GPT-5",
    "Claude-Sonnet-4",
    "Gemini-2.5-Pro",
    "Grok-4",
    "Qwen3-235B-A22B",
]

STANDARD_MODELS = [
    "GPT-5-mini",
    # "Claude-Sonnet-3.7",
    "Gemini-2.5-Flash",
    "Qwen3-235B-2507",
]

MODEL_PARAMS = {
    "Gemini-2.5-Flash": ["--web_search false", "--thinking_budget 0"],
    "GPT-5-mini": ["--reasoning_effort minimal"],
    "Claude-Sonnet-3.7": ["--thinking_budget 0"],
}

MODEL_IDS = {
    "Claude-Sonnet-4": "claude-opus-4-1-20250805",
    "Claude-Sonnet-3.7": "claude-3-7-sonnet-20250219",
    "Poe-Claude-Sonnet-3.7": "Claude-Sonnet-3.7",
    "Qwen3-235B-2507": "Qwen3-235B-2507-FW",
}

SAMPLE_MODELS = ["Sonoma-Sky-Alpha"]

JUDGE_MODEL = "GPT-5-mini"
