import os

from dotenv import load_dotenv
from poe_code_agent import PoeCodeAgent
from smolagents import OpenAIServerModel, models

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


def get_agent(model_id: str) -> PoeCodeAgent:
    agent_model = _get_agent_model(model_id)
    return PoeCodeAgent(tools=[], model=agent_model, verbosity_level=2)
