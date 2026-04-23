import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.tools.toolbox_toolset import ToolboxToolset

load_dotenv(Path(__file__).with_name(".env"))

toolbox = ToolboxToolset(
    server_url=os.getenv("TOOLBOX_SERVER_URL", "http://127.0.0.1:5000"),
    # toolset_name=os.getenv("TOOLBOX_TOOLSET", "demo-toolset"),
)

root_agent = Agent(
    model=os.getenv("ADK_MODEL", "gemini-2.5-flash"),
    name="root_agent",
    description="A helpful assistant that can call MCP Toolbox tools.",
    instruction=(
        "You are a helpful assistant. Prefer using available MCP Toolbox tools "
        "when external or real-time data is needed."
    ),
    tools=[toolbox],
)
