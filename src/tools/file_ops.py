from langchain_core.tools import tool


@tool
def read_file(path: str) -> str:
    """Read the contents of a file at the given path."""
    with open(path) as f:
        return f.read()


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path. Creates directories if needed."""
    import os

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return f"Written {len(content)} bytes to {path}"
