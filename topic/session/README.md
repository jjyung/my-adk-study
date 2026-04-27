# Topic: Session Management

This directory explores how to manage conversations, user state, and session persistence using the Google Agent Development Kit (ADK).

It demonstrates how to configure session storage backends, dynamically inject session state into agent prompts, and allow the agent to mutate its memory through tools.

## Key Concepts Demonstrated

### 1. Multi-Backend Session Persistence

The `session_factory.py` establishes a factory pattern to switch between different `SessionService` implementations based on the `SESSION_MODE` environment variable.

- **`in_memory`**: Ephemeral storage (default). Useful for quick testing where state resets between runs.
- **`database`**: Persistent SQL database storage (e.g., SQLite via `session.db`).
- **`vertex_ai`**: Cloud-native persistence leveraging Google Cloud Vertex AI Agent Engine.

### 2. State Mutation via Tools

The agent (`agent/agent.py`) is equipped with tools that interact directly with the `ToolContext.state`:

- `set_user_info`: Allows the agent to actively save profile information (like name or occupation) into the session context when the user provides it.
- `get_user_info`: Allows the agent to query what it currently remembers.

### 3. Dynamic Prompt Injection

The agent uses a dynamic `instruction` callable (`_build_instruction`) to inject the current user state straight into the system prompt:

```python
async def _build_instruction(readonly_context) -> str:
    base_instruction = "... Current user profile: {user:info?} ..."
    return await inject_session_state(base_instruction, readonly_context)
```

This ensures the agent is immediately aware of who it is talking to without having to actively use a tool on every turn.

## How to Test

You can easily switch the persistence layer by editing the `.env` file in this directory:

```env
SESSION_MODE=database
DB_URL=sqlite+aiosqlite:///session.db
```

### Try it out in the CLI

1. Start an interactive terminal session:

   ```bash
   make cli
   ```

2. Tell the agent your name (e.g., "Hi, my name is Alice"). The agent will use the `set_user_info` tool to remember it.
3. Exit the CLI (`/quit`).
4. Run `make cli` again.
5. Ask the agent "What is my name?" and it should remember you thanks to the persisted session state and dynamic prompt injection!

### Other Run Commands

- **Web UI**: Run `make web` to test the agent using the ADK visual web interface.
- **FastAPI API**: Run `make run` or `make dev` to start a production-like REST API endpoint that respects the session persistence configured by the factory.
