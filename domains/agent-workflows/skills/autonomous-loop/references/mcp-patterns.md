# MCP Patterns for Autonomous Loops

Model Context Protocol configuration patterns for efficient tool integration.

## The Token Budget Problem

MCP tool definitions consume context tokens. More than 20K tokens of MCPs significantly constrains working memory.

**Solution:** Use progressive disclosure and code execution patterns.

## Configuration Structure

```
~/.claude.json           # User-level config (personal tools)
./.mcp.json             # Project-level config (shared with team)
```

### Basic Server Definition

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Environment Variable Expansion

```json
{
  "env": {
    "API_KEY": "${API_KEY}",
    "DEBUG": "${DEBUG:-false}",
    "PORT": "${PORT:-3000}"
  }
}
```

## Essential Servers for Autonomous Loops

### Minimal Production Set

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/path/to/project"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    }
  }
}
```

### Extended Set (When Needed)

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres"],
      "env": {"DATABASE_URL": "${DATABASE_URL}"}
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-memory"]
    }
  }
}
```

## Progressive Disclosure Pattern

Instead of loading all tools upfront, discover on-demand:

### Tool Discovery Script

```python
#!/usr/bin/env python3
# scripts/discover_tools.py
"""Search available tools by keyword."""

import json
import sys

TOOL_REGISTRY = {
    "database": ["postgres", "sqlite", "mysql"],
    "browser": ["puppeteer", "playwright"],
    "git": ["github", "gitlab"],
    "file": ["filesystem", "s3"],
    "ai": ["anthropic", "openai"]
}

def search_tools(keyword: str):
    """Find tools matching keyword."""
    results = []
    for category, tools in TOOL_REGISTRY.items():
        if keyword.lower() in category:
            results.extend(tools)
        else:
            results.extend(t for t in tools if keyword.lower() in t)
    return results

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(search_tools(keyword)))
```

### CLAUDE.md Integration

```markdown
## Tool Discovery

When you need a tool not currently available:

1. Run: `python3 scripts/discover_tools.py <keyword>`
2. Check if the tool is in .mcp.json
3. If not, add it and restart with `/mcp restart <server>`

Available tool categories: database, browser, git, file, ai
```

## Code Execution Pattern

Present MCP servers as code APIs — agent discovers tools by exploring:

```python
#!/usr/bin/env python3
# scripts/mcp_wrapper.py
"""Thin wrapper exposing MCP tools as functions."""

import subprocess
import json

def call_tool(server: str, tool: str, params: dict) -> dict:
    """Call an MCP tool and return result."""
    # Implementation depends on MCP client library
    pass

def list_server_tools(server: str) -> list:
    """List tools available on a server."""
    pass
```

Benefits:
- Up to 98.7% reduction in token usage
- Tools loaded only when invoked
- Agent learns tool capabilities through code

## Context-Efficient Results

Filter and transform data before returning to model:

```python
def get_github_issues(repo: str, limit: int = 10) -> list:
    """Get issues with minimal fields."""
    raw_issues = call_tool("github", "list_issues", {"repo": repo})

    return [{
        "number": i["number"],
        "title": i["title"],
        "state": i["state"]
    } for i in raw_issues[:limit]]
```

## Scope Configuration

### User Scope (Personal Tools)

In `~/.claude.json`:

```json
{
  "mcpServers": {
    "personal-notes": {
      "command": "node",
      "args": ["/home/user/tools/notes-server.js"]
    }
  }
}
```

### Project Scope (Shared)

In `.mcp.json` (commit to git):

```json
{
  "mcpServers": {
    "project-db": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

Note: Credentials use environment variables, not hardcoded values.

## MCP Commands in Claude Code

| Command | Purpose |
|---------|---------|
| `/mcp` | Show server status |
| `/mcp restart <name>` | Restart a server |
| `/mcp logs <name>` | View server logs |

## Autonomous Loop Integration

### Startup Check Script

```bash
#!/bin/bash
# scripts/check_mcp.sh - Verify required servers

REQUIRED_SERVERS=("github" "filesystem")

for server in "${REQUIRED_SERVERS[@]}"; do
    if ! claude --mcp-status 2>/dev/null | grep -q "$server.*running"; then
        echo "ERROR: MCP server '$server' not running"
        exit 1
    fi
done

echo "All required MCP servers running"
```

### Progress Notes Integration

```markdown
## progress.txt

### MCP Status
- github: active, 15 calls this session
- filesystem: active
- postgres: disabled (not needed for current task)
```

## Performance Tips

1. **Disable unused servers** - Each server consumes baseline tokens
2. **Use `/mcp` to monitor** - Check which servers are active
3. **Batch operations** - Multiple tool calls in one request
4. **Cache results** - Store responses in files for reuse

## Common Issues

### Server Won't Start

```bash
# Check if port is in use
lsof -i :PORT

# Check server logs
claude /mcp logs <server-name>

# Restart with debug
DEBUG=* npx -y @anthropic/mcp-server-<name>
```

### Token Budget Exceeded

Symptoms: Agent becomes confused, forgets context

Solutions:
1. Reduce number of active servers
2. Use code execution pattern
3. Clear context more frequently
4. Filter tool result data

### Environment Variables Not Found

```bash
# Verify variable is set
echo $GITHUB_TOKEN

# Check .env file is sourced
source .env && claude

# Use default values
"${VAR:-default}"
```

## MCP for Browser Automation

Critical for verification in autonomous loops:

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"],
      "env": {
        "PUPPETEER_HEADLESS": "true",
        "PUPPETEER_TIMEOUT": "30000"
      }
    }
  }
}
```

### Verification Script

```python
#!/usr/bin/env python3
# scripts/verify_ui.py
"""Use Puppeteer MCP to verify UI changes."""

from mcp_wrapper import call_tool

def verify_feature(feature_id: str, test_url: str) -> bool:
    """Navigate to URL and verify feature works."""

    call_tool("puppeteer", "navigate", {"url": test_url})

    screenshot = call_tool("puppeteer", "screenshot", {})

    result = call_tool("puppeteer", "evaluate", {
        "script": f"document.querySelector('[data-feature=\"{feature_id}\"]') !== null"
    })

    return result.get("value", False)
```
