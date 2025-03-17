# tools/user_tools.py
from typing import Dict, Any

from mcp import Tool, AsyncToolFunction, ToolParam

from jira_client import jira_client

@Tool(
    name="get_user",
    description="Get user information by email",
    parameters=[
        ToolParam(name="email", type="string", description="User email")
    ]
)
async def get_user(email: str) -> Dict[str, Any]:
    """Get user information by email."""
    return await jira_client.get_user(email)
