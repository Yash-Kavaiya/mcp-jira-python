# jira_client.py
import os
from typing import Dict, Any, List, Optional

from jira import JIRA

class JiraClient:
    """Client for interacting with JIRA API."""
    
    def __init__(self, server: str, username: str, api_token: str):
        """Initialize JIRA client.
        
        Args:
            server: JIRA server URL
            username: JIRA username or email
            api_token: JIRA API token
        """
        self.jira = JIRA(
            server=server,
            basic_auth=(username, api_token)
        )
    
    async def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get issue by key.
        
        Args:
            issue_key: JIRA issue key (e.g., PROJ-123)
            
        Returns:
            Issue details as dictionary
        """
        issue = self.jira.issue(issue_key)
        
        # Convert to dict with relevant fields
        result = {
            "key": issue.key,
            "id": issue.id,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name,
            "issue_type": issue.fields.issuetype.name,
            "priority": issue.fields.priority.name if hasattr(issue.fields, "priority") and issue.fields.priority else None,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
            "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
            "created": issue.fields.created,
            "updated": issue.fields.updated,
            "comments": [
                {
                    "id": comment.id,
                    "body": comment.body,
                    "author": comment.author.displayName,
                    "created": comment.created
                }
                for comment in issue.fields.comment.comments
            ] if hasattr(issue.fields, "comment") else []
        }
        
        return result
    
    async def create_issue(self, 
                    project_key: str, 
                    summary: str, 
                    description: str,
                    issue_type: str,
                    priority: Optional[str] = None,
                    assignee_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new issue.
        
        Args:
            project_key: Project key (e.g., PROJ)
            summary: Issue summary
            description: Issue description
            issue_type: Issue type (e.g., Bug, Story)
            priority: Priority (e.g., High, Medium)
            assignee_id: Account ID of assignee
            
        Returns:
            Created issue details
        """
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        
        if priority:
            issue_dict['priority'] = {'name': priority}
        
        if assignee_id:
            issue_dict['assignee'] = {'accountId': assignee_id}
        
        new_issue = self.jira.create_issue(fields=issue_dict)
        
        return {
            "key": new_issue.key,
            "id": new_issue.id,
            "self": new_issue.self
        }
    
    async def update_issue(self,
                    issue_key: str,
                    summary: Optional[str] = None,
                    description: Optional[str] = None,
                    status: Optional[str] = None,
                    priority: Optional[str] = None,
                    assignee_id: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing issue.
        
        Args:
            issue_key: Issue key to update
            summary: New summary
            description: New description
            status: New status
            priority: New priority
            assignee_id: New assignee account ID
            
        Returns:
            Updated issue key
        """
        issue = self.jira.issue(issue_key)
        update_dict = {}
        
        if summary:
            update_dict['summary'] = summary
        
        if description:
            update_dict['description'] = description
        
        if priority:
            update_dict['priority'] = {'name': priority}
        
        if assignee_id:
            update_dict['assignee'] = {'accountId': assignee_id}
        
        if update_dict:
            issue.update(fields=update_dict)
        
        if status:
            transitions = self.jira.transitions(issue)
            for t in transitions:
                if t['name'].lower() == status.lower():
                    self.jira.transition_issue(issue, t['id'])
                    break
        
        return {"key": issue_key, "updated": True}
    
    async def delete_issue(self, issue_key: str) -> Dict[str, bool]:
        """Delete an issue.
        
        Args:
            issue_key: Issue key to delete
            
        Returns:
            Success status
        """
        self.jira.delete_issue(issue_key)
        return {"deleted": True}
    
    async def add_comment(self, issue_key: str, body: str) -> Dict[str, Any]:
        """Add a comment to an issue.
        
        Args:
            issue_key: Issue key
            body: Comment text
            
        Returns:
            Comment details
        """
        comment = self.jira.add_comment(issue_key, body)
        return {
            "id": comment.id,
            "body": comment.body,
            "author": comment.author.displayName,
            "created": comment.created
        }
    
    async def search_issues(self, jql: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for issues using JQL.
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results to return
            
        Returns:
            List of matching issues
        """
        issues = self.jira.search_issues(jql, maxResults=max_results)
        
        results = []
        for issue in issues:
            results.append({
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "issue_type": issue.fields.issuetype.name,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
                "updated": issue.fields.updated
            })
        
        return results
    
    async def get_user(self, email: str) -> Dict[str, Any]:
        """Get user information by email.
        
        Args:
            email: User email
            
        Returns:
            User details
        """
        users = self.jira.search_users(query=email)
        if not users:
            return {"found": False}
        
        user = users[0]
        return {
            "account_id": user.accountId,
            "display_name": user.displayName,
            "email": getattr(user, 'emailAddress', email),
            "active": user.active
        }
# Add to jira_client.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add error handling to methods
async def get_issue(self, issue_key: str) -> Dict[str, Any]:
    """Get issue by key with error handling."""
    try:
        issue = self.jira.issue(issue_key)
        # Rest of the method...
        return result
    except Exception as e:
        logger.error(f"Error getting issue {issue_key}: {str(e)}")
        return {"error": str(e), "issue_key": issue_key}
