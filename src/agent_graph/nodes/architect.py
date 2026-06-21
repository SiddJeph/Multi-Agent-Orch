import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.llm.client import get_llm


def architect_node(state: dict) -> dict:
    llm = get_llm()
    prompt = f"""You are a Software Architect. Analyze the following requirements and produce an architecture plan.

Requirements:
{state['requirements']}

Your plan must include:
1. Project structure (files and directories)
2. Component design and responsibilities
3. Data flow between components
4. Key technology choices
5. Implementation order

Output as a JSON object with keys: project_structure, components, data_flow, tech_choices, implementation_order
"""

    messages = [SystemMessage(content=prompt), HumanMessage(content=state["requirements"])]
    response = llm.invoke(messages)

    content = response.content if isinstance(response.content, str) else str(response.content)
    try:
        parsed = json.loads(content.replace("```json", "").replace("```", "").strip())
    except json.JSONDecodeError:
        parsed = {"raw": content}

    return {
        "messages": [AIMessage(content=response.content)],
        "architecture": json.dumps(parsed, indent=2),
        "status": "architecture_complete",
    }
