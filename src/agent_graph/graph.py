from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.agent_graph.state import CodeGenState
from src.agent_graph.nodes.architect import architect_node
from src.agent_graph.nodes.coder import coder_node
from src.agent_graph.nodes.reviewer import reviewer_node
from src.agent_graph.nodes.tester import tester_node
from src.agent_graph.nodes.documenter import documenter_node
from src.agent_graph.edges import should_retry_review, should_retry_test
from src.storage.persistence import get_checkpointer


def build_graph() -> CompiledStateGraph:
    workflow = StateGraph(CodeGenState)

    workflow.add_node("architect", architect_node)  # type: ignore[type-var]
    workflow.add_node("coder", coder_node)  # type: ignore[type-var]
    workflow.add_node("reviewer", reviewer_node)  # type: ignore[type-var]
    workflow.add_node("tester", tester_node)  # type: ignore[type-var]
    workflow.add_node("documenter", documenter_node)  # type: ignore[type-var]

    workflow.set_entry_point("architect")

    workflow.add_edge("architect", "coder")
    workflow.add_conditional_edges("reviewer", should_retry_review, {"coder": "coder", "tester": "tester"})
    workflow.add_conditional_edges("tester", should_retry_test, {"coder": "coder", "documenter": "documenter"})
    workflow.add_edge("coder", "reviewer")
    workflow.add_edge("documenter", END)

    checkpointer = get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)
