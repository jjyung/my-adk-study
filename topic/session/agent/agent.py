from typing import Any, Literal

from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.utils.instructions_utils import inject_session_state

USER_INFO_KEY = "user:info"
USER_INFO_FIELDS: tuple[str, str] = ("name", "occupation")


def _normalize_user_info(raw: Any) -> dict[str, str | None]:
    info = {"name": None, "occupation": None}
    if not isinstance(raw, dict):
        return info

    for field in USER_INFO_FIELDS:
        value = raw.get(field)
        if isinstance(value, str):
            cleaned = value.strip()
            info[field] = cleaned or None
    return info


def get_user_info(tool_context: ToolContext) -> dict[str, str | None]:
    """Returns the full user info model from user state."""
    return _normalize_user_info(tool_context.state.get(USER_INFO_KEY))


def set_user_info(
    field: Literal["name", "occupation"], value: str, tool_context: ToolContext
) -> dict[str, str | None]:
    """Updates one user info field and returns the full user info model."""
    if field not in USER_INFO_FIELDS:
        allowed = ", ".join(USER_INFO_FIELDS)
        raise ValueError(f"Invalid field '{field}'. Allowed fields: {allowed}")

    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError("Value cannot be empty.")

    info = get_user_info(tool_context)
    info[field] = cleaned_value
    tool_context.state[USER_INFO_KEY] = info
    return info


async def _build_instruction(readonly_context) -> str:
    base_instruction = """
You are a helpful assistant for user questions.

Current user profile (if available): {user:info?}

Tool-first memory rules:
- If user explicitly provides profile info (name or occupation), call set_user_info immediately.
- If user asks what you remember about them, call get_user_info before answering.
- If you are not sure whether a statement should be stored, ask a short clarification first.
- Do not invent or infer profile data that the user did not explicitly provide.
"""
    return await inject_session_state(base_instruction, readonly_context)


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction=_build_instruction,
    tools=[get_user_info, set_user_info],
)
