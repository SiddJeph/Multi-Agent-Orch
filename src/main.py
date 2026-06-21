import logging

import uvicorn
from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from src.api.routes import router
from src.agent_graph.graph import build_graph
from src.config import settings

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="Multi-Agent Code Orchestrator", version="0.1.0")
app.include_router(router)


@app.on_event("startup")
async def startup():
    logger.info("Starting Multi-Agent Code Orchestrator")
    logger.info("LLM Model: %s", settings.llm_model)


@app.get("/health")
async def health():
    return {"status": "ok"}


def cli():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "run-task":
        requirements = sys.argv[2] if len(sys.argv) > 2 else "Create a simple calculator in Python"
        graph = build_graph()
        config = {"configurable": {"thread_id": "cli-task"}}
        result = graph.invoke(
            {
                "messages": [HumanMessage(content=requirements)],
                "requirements": requirements,
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
        print(f"Status: {result['status']}")
        print(f"Architecture: {result['architecture'][:200]}...")
        print(f"Files created: {list(result['code'].keys())}")
        return

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    cli()
