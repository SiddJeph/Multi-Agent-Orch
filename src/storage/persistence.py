from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

from src.config import settings


def get_checkpointer():
    if settings.database_url.startswith("postgresql"):
        return PostgresSaver.from_conn_string(settings.database_url)
    return SqliteSaver.from_conn_string("checkpoints.db")
