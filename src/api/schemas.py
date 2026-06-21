from pydantic import BaseModel


class TaskRequest(BaseModel):
    requirements: str
    thread_id: str = "default"


class TaskResponse(BaseModel):
    thread_id: str
    status: str
    result: dict | None = None
    error: str | None = None
