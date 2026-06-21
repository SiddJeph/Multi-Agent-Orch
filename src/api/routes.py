from fastapi import APIRouter, HTTPException
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from src.agent_graph.graph import build_graph
from src.api.schemas import TaskRequest, TaskResponse
from src.agent_graph.state import CodeGenState

router = APIRouter(prefix="/api/v1")
_graph: CompiledStateGraph | None = None


def get_graph() -> CompiledStateGraph:
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def _make_config(thread_id: str) -> RunnableConfig:
    return {"configurable": {"thread_id": thread_id}}


@router.post("/tasks", response_model=TaskResponse)
async def create_task(req: TaskRequest):
    graph = get_graph()
    config = _make_config(req.thread_id)

    initial_state: CodeGenState = {
        "messages": [],
        "requirements": req.requirements,
        "architecture": "",
        "code": {},
        "review_feedback": [],
        "test_results": {},
        "documentation": "",
        "iteration_count": 0,
        "errors": [],
        "status": "started",
    }

    try:
        result = await graph.ainvoke(initial_state, config)
        return TaskResponse(
            thread_id=req.thread_id,
            status=result.get("status", "unknown"),
            result=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{thread_id}", response_model=TaskResponse)
async def get_task(thread_id: str):
    graph = get_graph()
    config = _make_config(thread_id)
    state = graph.get_state(config)
    if state is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        thread_id=thread_id,
        status=state.values.get("status", "unknown"),
        result=state.values,
    )
