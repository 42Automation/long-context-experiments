import argparse
import asyncio
import importlib.util
import json
import os
from datetime import datetime

from fastapi_poe import BotError

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


def record_output(experiment, model, output, passed, experiment_name):
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


async def main():
    parser = argparse.ArgumentParser(description="Run LLM experiments")
    parser.add_argument(
        "-e",
        "--experiment",
        type=str,
        required=True,
        help="Name of the experiment file (without .py) located in ./experiments/",
    )
    args = parser.parse_args()

    # Load experiments dynamically based on the CLI argument
    experiments = load_experiments(args.experiment)

    tasks = [
        run_experiment(experiment, model)
        for experiment in experiments
        for model in models
    ]

    results = await asyncio.gather(*tasks)
    for experiment, model, output, passed in results:
        record_output(experiment, model, output, passed, args.experiment)


if __name__ == "__main__":
    asyncio.run(main())
