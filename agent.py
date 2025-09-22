from models import MODEL_IDS
from prompts import RETRIEVAL_AGENT_DESCRIPTION_TEMPLATE
from rag import Retriever
from tools import RetrieverTool
from wrapped_agents import WrappedToolCallingAgent, get_agent_model


def get_agent_team(
    model_id: str, pdf_doc_urls: list[str], max_k: int
) -> WrappedToolCallingAgent:
    # Get model
    model_id = MODEL_IDS.get(model_id, model_id)
    agent_model = get_agent_model(model_id)

    # Get retriever
    retriever_tool = RetrieverTool()
    retriever = Retriever(pdf_doc_urls=pdf_doc_urls)
    retriever_tool.retriever = retriever

    # Get retriever agent
    retriever_agent = WrappedToolCallingAgent(
        tools=[retriever_tool],
        model=agent_model,
        max_steps=3,
        verbosity_level=2,
        name="retriever_agent",
        description=RETRIEVAL_AGENT_DESCRIPTION_TEMPLATE.format(max_k=max_k),
    )

    # Get manager agent
    manager_agent = WrappedToolCallingAgent(
        tools=[],
        model=agent_model,
        max_steps=6,
        verbosity_level=2,
        name="manager_agent",
        description="A manager agent, which specializes in answering tough financial questions, "
        + "and commands a retriever agent as needed,",
        managed_agents=[retriever_agent],
        planning_interval=3,
    )

    return manager_agent
