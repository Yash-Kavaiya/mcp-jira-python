# MCP-JIRA Python Server

A Python implementation of a Model Context Protocol (MCP) server for JIRA integration. This server enables AI assistants to interact with JIRA's API through a standardized interface.

## Features

- Full JIRA issue management (create, read, update, delete)
- Comment management with attachment support
- JQL-based issue searching
- User information retrieval
- MCP protocol compliance for seamless AI assistant integration
- Secure authentication with JIRA API tokens

## Prerequisites

- Python 3.8 or higher
- JIRA account with API access
- API token for authentication with JIRA
- Basic understanding of JIRA's REST API

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/mcp-jira-python.git
cd mcp-jira-python
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install mcp-python-sdk jira python-dotenv pydantic aiohttp
```

## Configuration

1. Create a `.env` file in the project root with your JIRA credentials:

```
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your.email@domain.com
JIRA_API_TOKEN=your_api_token
```

To obtain a JIRA API token:
1. Log in to your Atlassian account at https://id.atlassian.com/manage/api-tokens
2. Click "Create API token"
3. Name your token and click "Create"
4. Copy the token to your `.env` file

## Project Structure

```
mcp-jira-python/
├── main.py               # Entry point for the MCP server
├── jira_client.py        # JIRA API client implementation
├── tools/                # Implementation of MCP tools
│   ├── __init__.py
│   ├── issue_tools.py    # Issue-related operations
│   ├── search_tools.py   # Search functionality
│   └── user_tools.py     # User management operations
├── schema/               # Pydantic models for request/response validation
│   ├── __init__.py
│   └── models.py
├── test_client.py        # Simple client for testing the MCP server
├── .env                  # Environment variables (create this file)
└── README.md             # This file
```

## Running the Server

Start the MCP server by running:

```bash
python main.py
```

The server listens for MCP messages on stdin/stdout, making it compatible with applications that support the MCP protocol, such as Claude Desktop.

## Integration with AI Assistants

### Claude Desktop

To integrate with Claude Desktop:

1. Locate the Claude Desktop configuration file:
   - Windows: `%AppData%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Add the MCP server configuration:

```json
{
  "mcp_servers": [
    {
      "name": "JIRA Integration",
      "path": "path/to/your/main.py",
      "tools": [
        "get_issue",
        "create_issue",
        "update_issue",
        "delete_issue",
        "add_comment",
        "search_issues",
        "get_user"
      ]
    }
  ]
}
```

## Testing

Use the included test client to verify the server functionality:

```bash
python test_client.py
```

The test client sends sample requests to search for issues and create a new issue.

## API Documentation

### Available Tools

#### Issue Management

- **get_issue**: Retrieve detailed information about a JIRA issue
  - Parameters:
    - `issue_key` (string): The JIRA issue key (e.g., PROJ-123)

- **create_issue**: Create a new JIRA issue
  - Parameters:
    - `project_key` (string): The project key (e.g., PROJ)
    - `summary` (string): Issue summary
    - `description` (string): Issue description
    - `issue_type` (string): Issue type (e.g., Bug, Story)
    - `priority` (string, optional): Priority (e.g., High, Medium)
    - `assignee_id` (string, optional): Account ID of assignee

- **update_issue**: Update an existing JIRA issue
  - Parameters:
    - `issue_key` (string): The issue key to update
    - `summary` (string, optional): New summary
    - `description` (string, optional): New description
    - `status` (string, optional): New status
    - `priority` (string, optional): New priority
    - `assignee_id` (string, optional): New assignee account ID

- **delete_issue**: Delete a JIRA issue
  - Parameters:
    - `issue_key` (string): The issue key to delete

- **add_comment**: Add a comment to a JIRA issue
  - Parameters:
    - `issue_key` (string): The issue key
    - `body` (string): Comment text

- **add_comment_with_attachment**: Add a comment with an attachment
  - Parameters:
    - `issue_key` (string): The issue key
    - `body` (string): Comment text
    - `attachment_path` (string): Path to the attachment file

#### Search

- **search_issues**: Search for JIRA issues using JQL
  - Parameters:
    - `jql` (string): JQL query string
    - `max_results` (integer, optional): Maximum number of results to return (default: 10)

#### User Management

- **get_user**: Get user information by email
  - Parameters:
    - `email` (string): User email

## Example MCP Requests

### Search for Issues

```json
{
  "type": "function",
  "function": "search_issues",
  "id": "req1",
  "parameters": {
    "jql": "project = PROJ AND status = 'In Progress'",
    "max_results": 5
  }
}
```

### Create an Issue

```json
{
  "type": "function",
  "function": "create_issue",
  "id": "req2",
  "parameters": {
    "project_key": "PROJ",
    "summary": "Test issue from MCP",
    "description": "This is a test issue created via MCP",
    "issue_type": "Task",
    "priority": "Medium"
  }
}
```

### Update an Issue

```json
{
  "type": "function",
  "function": "update_issue",
  "id": "req3",
  "parameters": {
    "issue_key": "PROJ-123",
    "summary": "Updated summary",
    "status": "In Progress"
  }
}
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check that your JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN are correct in the .env file
   - Verify that your API token has not expired
   - Ensure you have the necessary permissions in JIRA

2. **Invalid JQL Query**
   - Validate your JQL syntax using the JIRA web interface
   - Ensure fields referenced in your query exist in your JIRA instance

3. **MCP Connection Issues**
   - Verify the path to the MCP server is correct in claude_desktop_config.json
   - Check that all dependencies are installed
   - Restart Claude Desktop after configuration changes

## Error Logging

The server logs errors to the console with details about what went wrong. Check the console output for error messages when troubleshooting.

## Customization

### Adding New Tools

To add a new tool:

1. Implement the functionality in the JiraClient class
2. Create a new function in the appropriate tools file with the @Tool decorator
3. Register the tool in main.py
4. Add the tool name to the MCP configuration in claude_desktop_config.json

## Security Considerations

- Store API tokens securely and never commit them to version control
- Consider implementing rate limiting to prevent API abuse
- The MCP server has access to your JIRA instance with the permissions of the provided API token

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [MCP Protocol](https://github.com/socketteer/mcp) - For defining the Model Context Protocol
- [Python JIRA](https://jira.readthedocs.io/en/master/) - For the JIRA API client

---
Answer from Perplexity: pplx.ai/share