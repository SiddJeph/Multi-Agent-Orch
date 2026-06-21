from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


class CodeGenState(TypedDict):
    messages: Annotated[list, add_messages]
    requirements: str
    architecture: str
    code: dict[str, str]
    review_feedback: list[str]
    test_results: dict[str, Any]
    documentation: str
    iteration_count: int
    errors: list[str]
    status: str
