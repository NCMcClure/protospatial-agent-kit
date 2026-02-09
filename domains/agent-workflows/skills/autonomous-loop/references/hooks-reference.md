# Hooks Reference

Complete reference for Claude Code hooks in autonomous agentic loops.

## Hook Lifecycle Events

| Event | Fires When | Common Uses |
|-------|------------|-------------|
| PreToolUse | Before tool execution | Block dangerous ops, validate params |
| PostToolUse | After tool completion | Auto-format, auto-test, logging |
| Stop | Claude finishes responding | Validate completion, prevent premature exit |
| Notification | Notifications shown | Custom alerting |

## Configuration Location

```
.claude/
├── hooks.json          # Hook definitions
└── scripts/
    ├── pre_tool.py     # PreToolUse handler
    ├── post_tool.py    # PostToolUse handler
    └── stop_check.py   # Stop handler
```

## Hook Definition Structure

```json
{
  "hooks": {
    "<EventName>": [{
      "matcher": "<tool-pattern>",
      "hooks": [{
        "type": "command",
        "command": "<shell-command>"
      }]
    }]
  }
}
```

## Stop Hook Patterns

### Pattern 1: Test Validation

Block exit until all tests pass:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "npm test --passWithNoTests 2>&1 | tail -1 | grep -q 'passed' && echo '{\"decision\":\"allow\"}' || echo '{\"decision\":\"block\",\"reason\":\"Tests failing\"}'"
      }]
    }]
  }
}
```

### Pattern 2: Feature Verification

Check feature_list.json for unverified claims:

```python
#!/usr/bin/env python3
# scripts/stop_check.py
import json
import subprocess
import sys

def main():
    with open("feature_list.json") as f:
        features = json.load(f)["features"]

    claimed_passing = [f for f in features if f.get("passes")]

    for feature in claimed_passing:
        test_file = f"tests/{feature['id']}.test.js"
        result = subprocess.run(
            ["npm", "test", "--", test_file],
            capture_output=True
        )
        if result.returncode != 0:
            print(json.dumps({
                "decision": "block",
                "reason": f"Feature {feature['id']} marked passing but tests fail"
            }))
            return 2

    print(json.dumps({"decision": "allow"}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Pattern 3: Prompt-Based Validation (Haiku)

Use LLM to evaluate completion:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "prompt",
        "prompt": "Evaluate task completion. Read feature_list.json and test results. Respond with JSON: {\"decision\": \"allow\"} if all marked features verified, or {\"decision\": \"block\", \"reason\": \"<explanation>\"} if not."
      }]
    }]
  }
}
```

## PostToolUse Hook Patterns

### Pattern 1: Auto-Format on Edit

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "prettier --write \"$CLAUDE_TOOL_ARG_file_path\" 2>/dev/null || true"
      }]
    }]
  }
}
```

### Pattern 2: Auto-Test After Changes

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npm test -- --findRelatedTests \"$CLAUDE_TOOL_ARG_file_path\" --passWithNoTests"
      }]
    }]
  }
}
```

### Pattern 3: Progress Logging

```python
#!/usr/bin/env python3
# scripts/log_progress.py
import os
import json
from datetime import datetime

tool = os.environ.get("CLAUDE_TOOL_NAME", "unknown")
file_path = os.environ.get("CLAUDE_TOOL_ARG_file_path", "")

log_entry = {
    "timestamp": datetime.now().isoformat(),
    "tool": tool,
    "file": file_path
}

with open(".claude/activity.log", "a") as f:
    f.write(json.dumps(log_entry) + "\n")
```

## PreToolUse Hook Patterns

### Pattern 1: Block Dangerous Operations

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo \"$CLAUDE_TOOL_ARG_command\" | grep -qE '(rm -rf|sudo|chmod 777)' && echo '{\"decision\":\"block\",\"reason\":\"Dangerous command blocked\"}' || echo '{\"decision\":\"allow\"}'"
      }]
    }]
  }
}
```

### Pattern 2: Block Commits Until Tests Pass

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "if echo \"$CLAUDE_TOOL_ARG_command\" | grep -q 'git commit'; then npm test && echo '{\"decision\":\"allow\"}' || echo '{\"decision\":\"block\",\"reason\":\"Tests must pass before commit\"}'; else echo '{\"decision\":\"allow\"}'; fi"
      }]
    }]
  }
}
```

### Pattern 3: Parameter Modification

Modify tool inputs before execution:

```python
#!/usr/bin/env python3
# scripts/sanitize_input.py
import os
import json

command = os.environ.get("CLAUDE_TOOL_ARG_command", "")

# Add safety flags to npm commands
if command.startswith("npm install"):
    command = command.replace("npm install", "npm install --ignore-scripts")

print(json.dumps({
    "decision": "allow",
    "updatedInput": {"command": command}
}))
```

## Exit Code Semantics

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| 0 | Success | Continue execution |
| 2 | Blocking error | Show stderr to Claude, may retry |
| Other | Non-blocking error | Log and continue |

## Environment Variables

Available in hook scripts:

| Variable | Description |
|----------|-------------|
| CLAUDE_TOOL_NAME | Name of tool being invoked |
| CLAUDE_TOOL_ARG_* | Tool arguments (e.g., CLAUDE_TOOL_ARG_file_path) |

## Best Practices

1. **Keep hooks fast** - Long hooks block the agent
2. **Return valid JSON** - Invalid JSON is ignored
3. **Use exit codes correctly** - 2 for blocking, 0 for allow
4. **Log sparingly** - Logs consume context
5. **Test hooks manually** - Run scripts directly first

## Complete Example: Autonomous Loop Hooks

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/scripts/pre_bash.py"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "prettier --write \"$CLAUDE_TOOL_ARG_file_path\" 2>/dev/null; npm test -- --findRelatedTests \"$CLAUDE_TOOL_ARG_file_path\" --passWithNoTests 2>/dev/null || true"
      }]
    }],
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/scripts/validate_completion.py"
      }]
    }]
  }
}
```
