# tools/search_tools.py
from typing import Dict, Any, List

from mcp import Tool, AsyncToolFunction, ToolParam

from jira_client import jira_client

@Tool(
    name="search_issues",
    description="Search for JIRA issues using JQL",
    parameters=[
        ToolParam(name="jql", type="string", description="JQL query string"),
        ToolParam(name="max_results", type="integer", description="Maximum number of results to return", required=False)
    ]
)
async def search_issues(jql: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search for JIRA issues using JQL."""
    return await jira_client.search_issues(jql, max_results)
