import json


from src.agent_graph.state import CodeGenState
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
