import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.llm.client import get_llm
from src.tools import read_file


def reviewer_node(state: dict) -> dict:
    llm = get_llm(temperature=0.1)

    code_summary = "\n\n".join(
        f"=== {path} ===\n{content}" for path, content in state.get("code", {}).items()
    )

    prompt = f"""You are a Senior Code Reviewer. Review the following code for:
1. Bugs and logic errors
2. Security vulnerabilities
3. Code style and best practices
4. Performance issues
5. Missing error handling

Code to review:
{code_summary}

Output a JSON object with keys: approved (bool), issues (list of dicts with severity/file/line/description), summary
"""

    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=f"Review this code:\n\n{code_summary}"),
    ]
    response = llm.invoke(messages)

    try:
        review = json.loads(response.content.replace("```json", "").replace("```", "").strip())
    except json.JSONDecodeError:
        review = {"approved": False, "issues": [], "summary": response.content}

    feedback = state.get("review_feedback", []) + [response.content]

    return {
        "messages": [AIMessage(content=response.content)],
        "review_feedback": feedback,
        "status": "reviewed",
    }
