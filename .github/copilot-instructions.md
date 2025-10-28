# Miki AI Agent - Development Instructions

## Architecture Overview

**Miki** is a LangChain-based AI agent system with dual interfaces: a web UI (FastAPI) and CLI. The agent uses Kimi (Moonshot) LLM with structured output enforcement and conversation memory.

### Core Components

- **Agent Layer** (`agent.py`): LangChain agent with `response_format` for structured outputs
- **HTTP Interface** (`http_server.py`): FastAPI server on port 8000 with web UI at `/` and API at `/api/input`
- **Tools** (`tools.py`): LangChain `@tool` decorated functions with `ToolRuntime[Context]` for context injection
- **Model** (`model.py`): ChatOpenAI configured for Kimi API with `SecretStr` for API keys
- **Memory** (`memory.py`): `InMemorySaver` checkpointer for conversation state (thread_id based)
- **Output** (`output_structure.py`): Dataclass defining agent response schema (enforced via `response_format`)

## Critical Patterns

- always write code in english
