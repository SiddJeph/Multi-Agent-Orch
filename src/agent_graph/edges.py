import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.agent_graph.state import CodeGenState
from src.agent_graph.nodes.architect import architect_node
from src.agent_graph.nodes.coder import coder_node
from src.agent_graph.nodes.reviewer import reviewer_node
from src.agent_graph.nodes.tester import tester_node
from src.agent_graph.nodes.documenter import documenter_node
from src.config import settings


def should_retry_review(state: CodeGenState) -> str:
    if state["iteration_count"] >= settings.max_iterations:
        return "tester"
    try:
        review = json.loads(state["review_feedback"][-1] if state["review_feedback"] else "{}")
        if isinstance(review, dict) and review.get("approved"):
            return "tester"
    except (json.JSONDecodeError, IndexError):
        pass
    return "coder"


def should_retry_test(state: CodeGenState) -> str:
    if state["iteration_count"] >= settings.max_iterations:
        return "documenter"
    results = state.get("test_results", {})
    if results.get("passed"):
        return "documenter"
    return "coder"
