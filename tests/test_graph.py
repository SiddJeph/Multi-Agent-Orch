from src.agent_graph.graph import build_graph
from src.config import settings


def test_graph_compiles():
    graph = build_graph()
    assert graph is not None
    nodes = graph.get_graph().nodes
    assert "architect" in nodes
    assert "coder" in nodes
    assert "reviewer" in nodes
    assert "tester" in nodes
    assert "documenter" in nodes


def test_max_iterations_default():
    assert settings.max_iterations == 3


def test_state_keys(mock_llm_architect):
    graph = build_graph()
    config = {"configurable": {"thread_id": "test-smoke"}}
    result = graph.invoke(
        {
            "messages": [],
            "requirements": "Create a hello world script",
            "architecture": "",
            "code": {},
            "review_feedback": [],
            "test_results": {},
            "documentation": "",
            "iteration_count": 0,
            "errors": [],
            "status": "started",
        },
        config,
    )
    assert "status" in result
    assert "architecture" in result
    assert "code" in result
    assert "test_results" in result
    assert "iteration_count" in result
