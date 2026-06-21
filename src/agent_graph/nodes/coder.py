import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.llm.client import get_llm
from src.tools import read_file, write_file
from src.config import settings


def coder_node(state: dict) -> dict:
    llm = get_llm().bind_tools([write_file, read_file])

    iteration_hint = ""
    if state["iteration_count"] > 0:
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

    return {
        "messages": [AIMessage(content=response.content)],
        "status": "coding_complete",
    }
