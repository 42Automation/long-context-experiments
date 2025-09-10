import argparse
import asyncio
import importlib.util
import json
import os
from datetime import datetime

from fastapi_poe import BotError

from llm import get_response
from models import (
    JUDGE_MODEL,
    MODEL_PARAMS,
    PREMIUM_MODELS,
    SAMPLE_MODELS,
    STANDARD_MODELS,
)
from prompts import JUDGE_PROMPT_TEMPLATE


async def judge(question, correct_answer, output) -> bool:
    query = JUDGE_PROMPT_TEMPLATE.format(
        question=question, correct_answer=correct_answer, output=output
    )

    if (params := MODEL_PARAMS.get(JUDGE_MODEL)) is not None:
        query = f"{query} {' '.join(params)}"

    response = await get_response(model=JUDGE_MODEL, query=query)
    # Get the last line, which effectively discards eventual thinking part
    last_line = next(
        (line for line in reversed(response["text"].splitlines()) if line.strip()), ""
    )
    return last_line.lower().strip() == "true"


async def run_experiment(experiment, model):
    print(f"Running experiment for {experiment.get('id')} -- {model}")
    query = experiment.get("query")

    if (params := MODEL_PARAMS.get(model)) is not None:
        query = f"{query} {' '.join(params)}"

    output = await get_response(
        model=model,
        query=query,
        doc_urls=experiment.get("docs"),
    )
    print(f"Judging output for {experiment.get('id')} -- {model}")
    try:
        passed = await judge(
            experiment.get("query"), experiment.get("expected_answer"), output["text"]
        )
    except BotError as error:
        print(f"Judge error: {str(error)}")
        passed = False

    return (
        experiment,
        model,
        output["text"],
        output["input_tokens"],
        passed,
    )


def record_output(experiment_name, experiment, model, output, input_tokens, passed):
    print(f"Recording output for {experiment.get('id')} -- {model}")

    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    dir_path = f"./out/{timestamp}_{experiment_name}"
    os.makedirs(dir_path, exist_ok=True)

    filename = f"{dir_path}/{experiment.get('id')}_{model}.json"

    record = {
        "id": experiment.get("id"),
        "query": experiment.get("query"),
        "model": model,
        "doc_urls": experiment.get("docs"),
        "expected_answer": experiment.get("expected_answer"),
        "output": output,
        "input_tokens": input_tokens,
        "passed": passed,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)


def load_experiments(experiment_name: str):
    module_path = f"./experiments/{experiment_name}.py"
    spec = importlib.util.spec_from_file_location("experiment_module", module_path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(f"Experiment file not found: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "EXPERIMENTS")


async def try_experiment(experiment, model):
    try:
        result = await run_experiment(experiment, model)
        return {
            "id": experiment.get("id"),
            "model": model,
            "result": result,
            "error": None,
        }
    except Exception as exc:
        return {
            "id": experiment.get("id"),
            "model": model,
            "result": None,
            "error": exc,
        }


async def main():
    parser = argparse.ArgumentParser(description="Run LLM experiments")
    parser.add_argument(
        "-e",
        "--experiment",
        type=str,
        required=True,
        help="Name of the experiment file (without .py) located in ./experiments/",
    )
    parser.add_argument(
        "-m",
        "--models",
        type=str,
        choices=["sample", "standard", "premium"],
        default="sample",
        help="Model set to run: 'sample', 'standard', or 'premium' (default: sample).",
    )
    args = parser.parse_args()
    experiment_name = args.experiment

    # Choose the appropriate model list based on the CLI flag
    if args.models == "sample":
        models = SAMPLE_MODELS
    elif args.models == "standard":
        models = STANDARD_MODELS
    elif args.models == "premium":
        models = PREMIUM_MODELS

    # Load experiments dynamically based on the CLI argument
    experiments = load_experiments(experiment_name)

    tasks = [
        try_experiment(experiment, model)
        for experiment in experiments
        for model in models
    ]

    results = await asyncio.gather(*tasks)
    for result in results:
        if result["error"] is not None:
            print(
                f"[ERROR] Experiment '{result['id']}' with model '{result['model']}' "
                f"failed: {result['error']}"
            )
        else:
            experiment, model, output, input_tokens, passed = result["result"]
            record_output(
                experiment_name, experiment, model, output, input_tokens, passed
            )


if __name__ == "__main__":
    asyncio.run(main())
