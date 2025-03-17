# schema/models.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class JiraIssueCreate(BaseModel):
    """Model for creating a JIRA issue."""
    project_key: str = Field(..., description="Project key (e.g., PROJ)")
    summary: str = Field(..., description="Issue summary")
    description: str = Field(..., description="Issue description")
    issue_type: str = Field(..., description="Issue type (e.g., Bug, Story)")
    priority: Optional[str] = Field(None, description="Priority (e.g., High, Medium)")
    assignee_id: Optional[str] = Field(None, description="Account ID of assignee")

class JiraIssueUpdate(BaseModel):
    """Model for updating a JIRA issue."""
    issue_key: str = Field(..., description="Issue key to update")
    summary: Optional[str] = Field(None, description="New summary")
    description: Optional[str] = Field(None, description="New description")
    status: Optional[str] = Field(None, description="New status")
    priority: Optional[str] = Field(None, description="New priority")
    assignee_id: Optional[str] = Field(None, description="New assignee account ID")

class JiraComment(BaseModel):
    """Model for a JIRA comment."""
    id: str = Field(..., description="Comment ID")
    body: str = Field(..., description="Comment text")
    author: str = Field(..., description="Comment author display name")
    created: str = Field(..., description="Creation timestamp")

class JiraIssue(BaseModel):
    """Model for a JIRA issue."""
    key: str = Field(..., description="Issue key")
    id: str = Field(..., description="Issue ID")
    summary: str = Field(..., description="Issue summary")
    description: Optional[str] = Field(None, description="Issue description")
    status: str = Field(..., description="Issue status")
    issue_type: str = Field(..., description="Issue type")
    priority: Optional[str] = Field(None, description="Issue priority")
    assignee: Optional[str] = Field(None, description="Assignee display name")
    reporter: Optional[str] = Field(None, description="Reporter display name")
    created: str = Field(..., description="Creation timestamp")
    updated: str = Field(..., description="Last update timestamp")
    comments: List[JiraComment] = Field(default_factory=list, description="Issue comments")

class JiraUser(BaseModel):
    """Model for a JIRA user."""
    account_id: str = Field(..., description="User account ID")
    display_name: str = Field(..., description="User display name")
    email: Optional[str] = Field(None, description="User email address")
    active: bool = Field(..., description="Whether the user is active")
