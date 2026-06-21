from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage


@pytest.fixture(autouse=True)
def _set_test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")


def _make_mock_llm(content: str = "") -> MagicMock:
    mock = MagicMock()
    response = AIMessage(content=content, tool_calls=[])
    mock.invoke.return_value = response
    mock.bind_tools.return_value = mock
    return mock


@pytest.fixture
def mock_llm() -> Generator[MagicMock, None, None]:
    mock = _make_mock_llm()
    with patch("src.llm.client.ChatGoogleGenerativeAI", return_value=mock):
        yield mock


@pytest.fixture
def mock_llm_architect() -> Generator[MagicMock, None, None]:
    mock = _make_mock_llm(
        content='{"project_structure": ["main.py"], "components": [], "data_flow": [], "tech_choices": [], "implementation_order": []}'
    )
    with patch("src.llm.client.ChatGoogleGenerativeAI", return_value=mock):
        yield mock
