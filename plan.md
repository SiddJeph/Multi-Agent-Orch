# Multi-Agent Code Orchestrator

**Stack**: Python 3.12 / LangGraph / Google Gemini / FastAPI / Kubernetes

## Architecture

User → [FastAPI Gateway] → [LangGraph Orchestrator]
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              Architect    Coder        Reviewer
                    │           │           │
                    └───────────┼───────────┘
                                ▼
                          Tester → Documenter → Output

## Agent Workflow

1. **Architect** — Parse requirements → architecture plan, file structure, tech choices
2. **Coder** — Implement code per architecture, file-by-file
3. **Reviewer** — Static analysis, security check, style, bug detection
4. **Tester** — Write & run unit tests, report pass/fail
5. **Documenter** — Generate README, docstrings, API docs

Conditional edges: Reviewer → Coder (if issues & iter < N) | Tester → Coder (if tests fail)

## Project Structure

```
multi-agent-code-orch/
├── src/
│   ├── agent_graph/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── nodes/         # Agent node implementations
│   │   └── edges.py       # Conditional routing
│   ├── tools/             # Tool registry (shell, file ops, code exec)
│   ├── llm/               # Gemini client
│   ├── api/               # FastAPI routes
│   ├── storage/           # Persistence layer
│   └── main.py            # Entry point
├── kubernetes/            # K8s manifests
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Key Patterns

- LangGraph state graph with typed state schema
- Structured LLM output via tool-calling (JSON mode)
- Tool registry for safe code execution (sandboxed)
- PostgreSQL checkpointer for state persistence / recovery
- Conditional routing with max iteration guard
- OpenTelemetry tracing across agent steps
