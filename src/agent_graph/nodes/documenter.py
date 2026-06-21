from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.llm.client import get_llm


def documenter_node(state: dict) -> dict:
    llm = get_llm(temperature=0.3)

    code_summary = "\n\n".join(
        f"=== {path} ===\n{content[:500]}" for path, content in state.get("code", {}).items()
    )

    prompt = f"""You are a Technical Writer. Generate documentation for the project.

Architecture:
{state['architecture']}

Code files (truncated):
{code_summary}

Generate:
1. README.md — project overview, setup, usage
2. API documentation — endpoints, request/response formats
3. Setup guide — dependencies, environment variables, how to run
"""

    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content="Generate documentation for the project"),
    ]
    response = llm.invoke(messages)

    return {
        "messages": [AIMessage(content=response.content)],
        "documentation": response.content,
        "status": "documented",
    }
