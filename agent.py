import os

from dotenv import load_dotenv
from smolagents import OpenAIServerModel, models

from poe_code_agent import PoeCodeAgent
from prompts import RETRIEVAL_AGENT_DESCRIPTION_TEMPLATE
from tools import RetrieverTool

load_dotenv()

# Monkey patch the function which describes whether model supports stop parameters
# to always return False.
# This effectively prevents the Poe API call from failing on some models
models.supports_stop_parameter = lambda model_id: False

POE_API_KEY = os.environ.get("POE_API_KEY", "")
if not POE_API_KEY:
    raise ValueError("Could not find POE_API_KEY variable in the environment")
POE_BASE_URL = os.environ.get("POE_BASE_URL", "")
if not POE_BASE_URL:
    raise ValueError("Could not find POE_BASE_URL variable in the environment")


def _get_agent_model(model_id: str) -> OpenAIServerModel:
    return OpenAIServerModel(
        model_id=model_id, api_base=POE_BASE_URL, api_key=POE_API_KEY
    )


def get_agent_team(model_id: str, pdf_doc_urls: list[str], max_k: int) -> PoeCodeAgent:
    agent_model = _get_agent_model(model_id)

    retrieval_agent = PoeCodeAgent(
        model=agent_model,
        tools=RetrieverTool(pdf_doc_urls=pdf_doc_urls),
        max_steps=3,
        verbosity_level=2,
        name="retriever_agent",
        description=RETRIEVAL_AGENT_DESCRIPTION_TEMPLATE.format(max_k=max_k),
    )

    manager_agent = PoeCodeAgent(
        model=agent_model,
        max_steps=6,
        verbosity_level=2,
        managed_agents=[retrieval_agent],
        planning_interval=3,
    )

    return manager_agent
