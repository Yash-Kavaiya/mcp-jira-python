# main.py
import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from mcp import MCP, Tool, AsyncToolFunction, ToolParam, ToolScope

from jira_client import JiraClient
from tools.issue_tools import get_issue, create_issue, update_issue, delete_issue, add_comment
from tools.search_tools import search_issues
from tools.user_tools import get_user

# Load environment variables
load_dotenv()

# Initialize JIRA client
jira_client = JiraClient(
    server=os.getenv("JIRA_URL"),
    username=os.getenv("JIRA_USERNAME"),
    api_token=os.getenv("JIRA_API_TOKEN")
)

# Initialize MCP server
mcp_server = MCP()

# Register tools
mcp_server.register_tool(get_issue)
mcp_server.register_tool(create_issue)
mcp_server.register_tool(update_issue)
mcp_server.register_tool(delete_issue)
mcp_server.register_tool(add_comment)
mcp_server.register_tool(search_issues)
mcp_server.register_tool(get_user)

# Start the MCP server using stdio transport
async def main():
    await mcp_server.start_stdio()

if __name__ == "__main__":
    asyncio.run(main())
