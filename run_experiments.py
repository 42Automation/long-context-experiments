import asyncio
import json
from datetime import datetime

from fastapi_poe import BotError

from experiments import EXPERIMENTS
from llm import LLM
from models import JUDGE_MODEL, MODEL_PARAMS, SAMPLE_MODELS
from prompts import JUDGE_PROMPT_TEMPLATE

llm = LLM()
models = SAMPLE_MODELS


async def judge(question, correct_answer, output) -> bool:
    query = JUDGE_PROMPT_TEMPLATE.format(
        question=question, correct_answer=correct_answer, output=output
    )
    response = await llm.get_response(model=JUDGE_MODEL, query=query)
    # Get the last line, which effectively discards eventual thinking part
    last_line = next(
        (line for line in reversed(response.splitlines()) if line.strip()), ""
    )
    return last_line.lower().strip() == "true"


async def run_experiment(experiment, model):
    print(f"Running experiment for {experiment.get('id')} -- {model}")
    query = experiment.get("query")

    if (params := MODEL_PARAMS.get(model)) is not None:
        query = f"{query} {' '.join(params)}"

    output = await llm.get_response(
        model=model,
        query=query,
        doc_urls=experiment.get("docs"),
    )
    print(f"Judging output for {experiment.get('id')} -- {model}")
    try:
        passed = await judge(
            experiment.get("query"), experiment.get("expected_answer"), output
        )
    except BotError as error:
        print(f"Judge error: {str(error)}")
        passed = False

    return experiment, model, output, passed


def record_output(experiment, model, output, passed):
    print(f"Recording output for {experiment.get('id')} -- {model}")
    record = {
        "id": experiment.get("id"),
        "query": experiment.get("query"),
        "model": model,
        "doc_urls": experiment.get("docs"),
        "expected_answer": experiment.get("expected_answer"),
        "output": output,
        "passed": passed,
    }

    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = f"./out/{timestamp}_{experiment.get('id')}_{model}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)


async def main():
    tasks = [
        run_experiment(experiment, model)
        for experiment in EXPERIMENTS
        for model in models
    ]

    results = await asyncio.gather(*tasks)
    for experiment, model, output, passed in results:
        record_output(experiment, model, output, passed)


if __name__ == "__main__":
    asyncio.run(main())
