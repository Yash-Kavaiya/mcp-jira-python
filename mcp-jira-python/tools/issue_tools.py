# tools/issue_tools.py
from typing import Dict, Any, Optional

from mcp import Tool, AsyncToolFunction, ToolParam

from jira_client import jira_client

@Tool(
    name="get_issue",
    description="Get detailed information about a JIRA issue",
    parameters=[
        ToolParam(name="issue_key", type="string", description="The JIRA issue key (e.g., PROJ-123)")
    ]
)
async def get_issue(issue_key: str) -> Dict[str, Any]:
    """Get detailed information about a JIRA issue."""
    return await jira_client.get_issue(issue_key)

@Tool(
    name="create_issue",
    description="Create a new JIRA issue",
    parameters=[
        ToolParam(name="project_key", type="string", description="The project key (e.g., PROJ)"),
        ToolParam(name="summary", type="string", description="Issue summary"),
        ToolParam(name="description", type="string", description="Issue description"),
        ToolParam(name="issue_type", type="string", description="Issue type (e.g., Bug, Story)"),
        ToolParam(name="priority", type="string", description="Priority (e.g., High, Medium)", required=False),
        ToolParam(name="assignee_id", type="string", description="Account ID of assignee", required=False)
    ]
)
async def create_issue(project_key: str, summary: str, description: str, issue_type: str, 
                       priority: Optional[str] = None, assignee_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new JIRA issue."""
    return await jira_client.create_issue(
        project_key=project_key,
        summary=summary,
        description=description,
        issue_type=issue_type,
        priority=priority,
        assignee_id=assignee_id
    )

@Tool(
    name="update_issue",
    description="Update an existing JIRA issue",
    parameters=[
        ToolParam(name="issue_key", type="string", description="The issue key to update"),
        ToolParam(name="summary", type="string", description="New summary", required=False),
        ToolParam(name="description", type="string", description="New description", required=False),
        ToolParam(name="status", type="string", description="New status", required=False),
        ToolParam(name="priority", type="string", description="New priority", required=False),
        ToolParam(name="assignee_id", type="string", description="New assignee account ID", required=False)
    ]
)
async def update_issue(issue_key: str, summary: Optional[str] = None, description: Optional[str] = None,
                       status: Optional[str] = None, priority: Optional[str] = None, 
                       assignee_id: Optional[str] = None) -> Dict[str, Any]:
    """Update an existing JIRA issue."""
    return await jira_client.update_issue(
        issue_key=issue_key,
        summary=summary,
        description=description,
        status=status,
        priority=priority,
        assignee_id=assignee_id
    )

@Tool(
    name="delete_issue",
    description="Delete a JIRA issue",
    parameters=[
        ToolParam(name="issue_key", type="string", description="The issue key to delete")
    ]
)
async def delete_issue(issue_key: str) -> Dict[str, bool]:
    """Delete a JIRA issue."""
    return await jira_client.delete_issue(issue_key)

@Tool(
    name="add_comment",
    description="Add a comment to a JIRA issue",
    parameters=[
        ToolParam(name="issue_key", type="string", description="The issue key"),
        ToolParam(name="body", type="string", description="Comment text")
    ]
)
async def add_comment(issue_key: str, body: str) -> Dict[str, Any]:
    """Add a comment to a JIRA issue."""
    return await jira_client.add_comment(issue_key, body)
