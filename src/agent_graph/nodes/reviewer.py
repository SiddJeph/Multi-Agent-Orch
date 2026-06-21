import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.llm.client import get_llm


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

    content = response.content if isinstance(response.content, str) else str(response.content)
    try:
        json.loads(content.replace("```json", "").replace("```", "").strip())
    except json.JSONDecodeError:
        pass

    feedback = state.get("review_feedback", []) + [content]

    return {
        "messages": [AIMessage(content=content)],
        "review_feedback": feedback,
        "status": "reviewed",
    }
