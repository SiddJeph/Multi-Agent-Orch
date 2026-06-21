from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage

from src.llm.client import get_llm
from src.tools import run_python, write_file


def tester_node(state: dict) -> dict:
    llm = get_llm().bind_tools([run_python, write_file])

    code_summary = "\n\n".join(
        f"=== {path} ===\n{content}" for path, content in state.get("code", {}).items()
    )

    prompt = f"""You are a QA Engineer. Write and run tests for the following code.

Code to test:
{code_summary}

1. Write unit tests for the key functions using the write_file tool
2. Use the run_python tool to execute the tests
3. Report pass/fail results
4. If tests fail, identify the issues
"""

    messages: list[BaseMessage] = [
        SystemMessage(content=prompt),
        HumanMessage(content=f"Write and run tests for:\n\n{code_summary}"),
    ]

    all_messages: list[BaseMessage] = []
    passed = False
    response = llm.invoke(messages)
    all_messages.append(response)

    max_rounds = 3
    for _ in range(max_rounds):
        if not response.tool_calls:
            break
        for tc in response.tool_calls:
            if tc["name"] == "run_python":
                result = run_python.invoke(tc["args"])
            elif tc["name"] == "write_file":
                result = write_file.invoke(tc["args"])
            else:
                result = f"Unknown tool: {tc['name']}"
            all_messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        response = llm.invoke(messages + all_messages)
        all_messages.append(response)

    last_output: str = ""
    for msg in reversed(all_messages):
        if isinstance(msg, ToolMessage):
            mc = msg.content if isinstance(msg.content, str) else str(msg.content)
            if "FAILED" in mc or "failed" in mc.lower():
                passed = False
                last_output = mc
                break
            if "passed" in mc.lower() or "OK" in mc:
                passed = True
                last_output = mc
                break
    else:
        last_content = all_messages[-1].content if all_messages else ""
        last_output = last_content if isinstance(last_content, str) else str(last_content)
        passed = "passed" in last_output.lower() and "failed" not in last_output.lower()

    results = state.get("test_results", {})
    results["last_run"] = last_output
    results["passed"] = passed

    return {
        "messages": all_messages,
        "test_results": results,
        "status": "tested",
    }
