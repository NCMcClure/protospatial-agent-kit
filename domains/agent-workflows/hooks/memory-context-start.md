# Memory Context Start Hook

Reminds Claude to read the memory system index at the start of each session. This is the read-side complement to the memory-capture-stop hook's write-side enforcement.

## How It Works

1. On session start, the hook checks if a memory directory exists in the project
2. If the directory and index file exist, it outputs a reminder for Claude to read the index
3. If no memory directory exists, the hook exits silently (project doesn't use memory)

## Settings Configuration

Add to `.claude/settings.local.json` or `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/memory_context_start.py"
          }
        ]
      }
    ]
  }
}
```

## Python Script

Place at `.claude/hooks/memory_context_start.py` in the target project:

```python
#!/usr/bin/env python3
"""
Memory context start hook.
Reminds Claude to read the memory index at session start.

Checks for memory directory existence and outputs a context-loading reminder.
Silently exits if no memory system is configured.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def load_config():
    """Load memory directory path from config, with fallback."""
    config_paths = [
        Path("memory_config.json"),
        Path(".claude/memory_config.json"),
    ]
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    config = json.load(f)
                return config.get("memory_dir", "memories")
            except (json.JSONDecodeError, IOError):
                pass
    return "memories"


def find_stale_files(memory_dir, days_threshold=30):
    """Find memory files not modified in the last N days."""
    stale = []
    now = datetime.now(timezone.utc)
    memory_path = Path(memory_dir)

    for md_file in memory_path.rglob("*.md"):
        if md_file.name == "index.md":
            continue
        try:
            mtime = datetime.fromtimestamp(md_file.stat().st_mtime, tz=timezone.utc)
            age_days = (now - mtime).days
            if age_days > days_threshold:
                relative = md_file.relative_to(memory_path)
                stale.append((str(relative), age_days))
        except OSError:
            continue

    return stale


def main():
    memory_dir = load_config()
    memory_path = Path(memory_dir)
    index_path = memory_path / "index.md"

    if not memory_path.exists() or not index_path.exists():
        # No memory system configured, exit silently
        return

    messages = [f"Memory system active. Read {memory_dir}/index.md for project context."]

    # Check for stale files
    stale = find_stale_files(memory_dir)
    if stale:
        stale_names = [f"{name} ({days}d)" for name, days in stale[:3]]
        messages.append(f"Stale memories: {', '.join(stale_names)}")

    print(" | ".join(messages))


if __name__ == "__main__":
    main()
```

## Behavior

**When memory exists:**
```
Memory system active. Read memories/index.md for project context. | Stale memories: technical/environment.md (45d), project/roadmap.md (32d)
```

**When no memory exists:**
No output (silent exit).

## Staleness Detection

The hook checks for memory files not modified in the last 30 days and surfaces up to 3 stale files in its output. This serves as a passive maintenance reminder — the user sees which files need attention without needing to run `/review-memory`.

The threshold is not configurable in this hook to keep it simple. For detailed staleness analysis, use the `/review-memory` command.

## Coexistence with Other Session Start Hooks

This hook coexists with other SessionStart hooks. Add it as a separate entry:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{"type": "command", "command": "python .claude/hooks/session_start.py"}]
      },
      {
        "hooks": [{"type": "command", "command": "python .claude/hooks/memory_context_start.py"}]
      }
    ]
  }
}
```
