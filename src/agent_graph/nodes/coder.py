from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from src.llm.client import get_llm
from src.tools import read_file, write_file
from src.config import settings


def coder_node(state: dict) -> dict:
    iteration_count = state.get("iteration_count", 0) + 1
    llm = get_llm().bind_tools([write_file, read_file])

    iteration_hint = ""
    if iteration_count > 1:
        feedback = "\n".join(state["review_feedback"][-3:])
        iteration_hint = f"\n\nPrevious review feedback to address:\n{feedback}"

    prompt = f"""You are a Senior Software Engineer. Implement the code based on the architecture plan below.

Architecture Plan:
{state['architecture']}
{iteration_hint}

Rules:
- Write complete, production-quality code
- Use the write_file tool to create each file
- Read existing files if you need to understand what's already there
- Structure the code according to the architecture plan
- Output the list of files you created
"""

    messages = [SystemMessage(content=prompt), HumanMessage(content=state["requirements"])]
    response = llm.invoke(messages)

    tool_messages = []
    if response.tool_calls:
        for tc in response.tool_calls:
            if tc["name"] == "write_file":
                result = write_file.invoke(tc["args"])
            elif tc["name"] == "read_file":
                result = read_file.invoke(tc["args"])
            else:
                result = f"Unknown tool: {tc['name']}"
            tool_messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

    code = {}
    workspace = Path(settings.workspace_dir)
    if workspace.exists():
        for fpath in sorted(workspace.rglob("*")):
            if fpath.is_file():
                code[str(fpath.relative_to(workspace))] = fpath.read_text()

    return {
        "messages": [AIMessage(content=response.content)] + tool_messages,
        "code": code,
        "iteration_count": iteration_count,
        "status": "coding_complete",
    }
