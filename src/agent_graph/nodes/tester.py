from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.llm.client import get_llm
from src.tools import run_python


def tester_node(state: dict) -> dict:
    llm = get_llm().bind_tools([run_python])

    code_summary = "\n\n".join(
        f"=== {path} ===\n{content}" for path, content in state.get("code", {}).items()
    )

    prompt = f"""You are a QA Engineer. Write and run tests for the following code.

Code to test:
{code_summary}

1. Write unit tests for the key functions
2. Use the run_python tool to execute them
3. Report pass/fail results
4. If tests fail, identify the issues
"""

    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=f"Write and run tests for:\n\n{code_summary}"),
    ]
    response = llm.invoke(messages)

    results = state.get("test_results", {})
    results["last_run"] = response.content

    return {
        "messages": [AIMessage(content=response.content)],
        "test_results": results,
        "status": "tested",
    }
