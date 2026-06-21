from langgraph.checkpoint.memory import MemorySaver

from src.config import settings


def get_checkpointer():
    try:
        from langgraph.checkpoint.postgres import PostgresSaver

        if settings.database_url.startswith("postgresql"):
            return PostgresSaver.from_conn_string(settings.database_url)
    except ImportError:
        pass
    return MemorySaver()
