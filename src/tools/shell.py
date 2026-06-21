import subprocess
import tempfile
from pathlib import Path

from langchain_core.tools import tool


@tool
def run_command(command: str, workdir: str | None = None) -> str:
    """Run a shell command and return its output. Use for listing files, running tests, etc."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=60,
        cwd=workdir or str(Path.cwd() / "workspace"),
    )
    output = result.stdout
    if result.returncode != 0:
        output += f"\n[exit code: {result.returncode}]\n{result.stderr}"
    return output


@tool
def run_python(code: str) -> str:
    """Run Python code in a sandboxed temp directory and return stdout/stderr."""
    with tempfile.TemporaryDirectory(prefix="sandbox_") as tmpdir:
        script = Path(tmpdir) / "script.py"
        script.write_text(code)
        result = subprocess.run(
            ["python", str(script)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=tmpdir,
        )
        output = result.stdout
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]\n{result.stderr}"
        return output
