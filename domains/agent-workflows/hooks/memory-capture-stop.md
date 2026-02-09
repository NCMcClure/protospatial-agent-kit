# Memory Capture Stop Hook

The enforcement mechanism for progressive disclosure memory systems. This Stop hook blocks session exit when meaningful work was done but memory wasn't updated — ensuring that institutional knowledge is captured before it's lost to context window boundaries.

## How It Works

1. When Claude tries to stop, the hook reads the session transcript
2. It scans for meaningful work keywords (deterministic, not LLM-judged)
3. It checks whether any memory files were written or edited during the session
4. If meaningful work happened AND memory wasn't updated → blocks exit with routing guidance
5. If no meaningful work OR memory was already updated → allows exit

## Why Deterministic?

The hook uses keyword matching, not AI judgment. This is intentional:
- **Predictable:** The user always knows why the hook fired
- **No false positives:** No subjective "importance" assessment
- **Debuggable:** Add a keyword to the list, see immediate effect
- **Consistent:** Same inputs always produce same outputs

The alternative — asking Claude "was this session important enough to persist?" — is subjective, inconsistent, and can be rationalized away.

## Settings Configuration

Add to `.claude/settings.local.json` or `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/memory_capture_stop.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

## Optional Configuration File

Place `memory_config.json` in the project root to customize behavior. If this file doesn't exist, the script uses built-in defaults.

```json
{
  "memory_dir": "memories",
  "meaningful_keywords": [
    "implemented", "fixed", "created", "updated", "refactored",
    "discovered", "learned", "solution", "approach", "decision",
    "resolved", "analyzed", "debugged", "designed", "architected",
    "chose", "migrated", "optimized", "integrated"
  ],
  "routing": {
    "technical": [
      "implemented", "fixed", "debugged", "refactored", "optimized",
      "migrated", "integrated", "resolved", "analyzed"
    ],
    "project": [
      "decision", "approach", "designed", "architected", "chose"
    ],
    "creative": [
      "created", "updated", "learned", "discovered"
    ]
  }
}
```

**Fields:**
- `memory_dir`: Path to the memory directory (default: `"memories"`)
- `meaningful_keywords`: Words that indicate meaningful work happened (case-insensitive scan)
- `routing`: Maps category names to keywords for routing guidance (tells the user which directory to update based on what kind of work was detected)

## Python Script

Place at `.claude/hooks/memory_capture_stop.py` in the target project:

```python
#!/usr/bin/env python3
"""
Memory capture stop hook.
Blocks session exit when meaningful work was done but memory wasn't updated.

Uses deterministic keyword scanning — not LLM judgment — to detect
meaningful work and check for memory updates.

Input: JSON via stdin with transcript_path or transcript content
Output: JSON with decision (allow/block) and optional reason
"""

import json
import sys
from pathlib import Path


# Built-in defaults used when no memory_config.json exists
DEFAULT_MEMORY_DIR = "memories"
DEFAULT_KEYWORDS = [
    "implemented", "fixed", "created", "updated", "refactored",
    "discovered", "learned", "solution", "approach", "decision",
    "resolved", "analyzed", "debugged", "designed", "architected",
    "chose", "migrated", "optimized", "integrated",
]
DEFAULT_ROUTING = {
    "technical": [
        "implemented", "fixed", "debugged", "refactored", "optimized",
        "migrated", "integrated", "resolved", "analyzed",
    ],
    "project": [
        "decision", "approach", "designed", "architected", "chose",
    ],
    "creative": [
        "created", "updated", "learned", "discovered",
    ],
}


def load_config():
    """Load configuration from memory_config.json, falling back to defaults."""
    config_paths = [
        Path("memory_config.json"),
        Path(".claude/memory_config.json"),
    ]
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    config = json.load(f)
                return {
                    "memory_dir": config.get("memory_dir", DEFAULT_MEMORY_DIR),
                    "keywords": config.get("meaningful_keywords", DEFAULT_KEYWORDS),
                    "routing": config.get("routing", DEFAULT_ROUTING),
                }
            except (json.JSONDecodeError, IOError):
                pass

    return {
        "memory_dir": DEFAULT_MEMORY_DIR,
        "keywords": DEFAULT_KEYWORDS,
        "routing": DEFAULT_ROUTING,
    }


def get_transcript(input_data):
    """Extract transcript content from hook input."""
    # Try transcript_path first (file-based)
    transcript_path = input_data.get("transcript_path", "")
    if transcript_path and Path(transcript_path).exists():
        try:
            return Path(transcript_path).read_text(encoding="utf-8")
        except (IOError, UnicodeDecodeError):
            return ""

    # Fall back to inline transcript content
    return input_data.get("transcript", "")


def find_matched_keywords(transcript_lower, keywords):
    """Find which meaningful keywords appear in the transcript."""
    return [kw for kw in keywords if kw in transcript_lower]


def check_memory_updated(transcript, memory_dir):
    """Check if memory files were written/edited during the session."""
    memory_marker = f"{memory_dir}/"
    has_memory_path = memory_marker in transcript
    has_write_op = "Write" in transcript or "Edit" in transcript
    return has_memory_path and has_write_op


def build_routing_guidance(matched_keywords, routing, memory_dir):
    """Build routing guidance based on which keywords were matched."""
    suggested_dirs = set()
    for category, category_keywords in routing.items():
        if any(kw in matched_keywords for kw in category_keywords):
            suggested_dirs.add(category)

    if not suggested_dirs:
        # Default to the first routing category if no specific match
        suggested_dirs.add(next(iter(routing), "project"))

    lines = [
        "Meaningful work detected but memory not updated.",
        f"Detected keywords: {', '.join(matched_keywords[:5])}",
        "",
        "Please update the relevant memory file before ending the session:",
    ]

    for dir_name in sorted(suggested_dirs):
        lines.append(f"  - {memory_dir}/{dir_name}/")

    lines.extend([
        "",
        "If no appropriate file exists, create one with a Quick Summary header.",
        "If there are no significant learnings to capture, you may stop.",
    ])

    return "\n".join(lines)


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # No valid input, allow stopping
        sys.exit(0)

    # Prevent infinite loops if the hook blocks and Claude retries
    if input_data.get("stop_hook_active", False):
        sys.exit(0)

    config = load_config()
    transcript = get_transcript(input_data)

    if not transcript:
        # No transcript available, allow stopping
        sys.exit(0)

    transcript_lower = transcript.lower()

    # Step 1: Check for meaningful work
    matched = find_matched_keywords(transcript_lower, config["keywords"])
    if not matched:
        # No meaningful work detected, allow stopping
        sys.exit(0)

    # Step 2: Check if memory was already updated
    if check_memory_updated(transcript, config["memory_dir"]):
        # Memory was updated, allow stopping
        sys.exit(0)

    # Step 3: Block — meaningful work done but memory not updated
    reason = build_routing_guidance(matched, config["routing"], config["memory_dir"])
    output = {"decision": "block", "reason": reason}
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
```

## Behavior Examples

### Meaningful work, no memory update → BLOCK
```
Claude: "I implemented the auth middleware and fixed the token refresh bug."
Hook: Detects "implemented", "fixed" → checks for memory write → none found → BLOCK

Output:
Meaningful work detected but memory not updated.
Detected keywords: implemented, fixed
Please update the relevant memory file before ending the session:
  - memories/technical/
If no appropriate file exists, create one with a Quick Summary header.
If there are no significant learnings to capture, you may stop.
```

### Meaningful work, memory already updated → ALLOW
```
Claude: "I implemented the auth middleware and updated memories/technical/issues-solutions.md"
Hook: Detects "implemented" → checks for memory write → found "memories/" + "Write" → ALLOW
```

### No meaningful work → ALLOW
```
Claude: "I read through the codebase and answered the user's questions."
Hook: No meaningful keywords found → ALLOW
```

## Coexistence with Other Stop Hooks

This hook coexists with autonomous loop validation hooks. Add it as a separate entry:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [{"type": "command", "command": "python .claude/hooks/validate_completion.py"}]
      },
      {
        "hooks": [{"type": "command", "command": "python .claude/hooks/memory_capture_stop.py", "timeout": 60}]
      }
    ]
  }
}
```

Both hooks run independently. The loop validation hook checks task completion; the memory hook checks knowledge capture. A session must satisfy both to exit.

## Customization Guide

### Adding Keywords

Add domain-specific keywords to catch work patterns unique to your project:

```json
{
  "meaningful_keywords": [
    "implemented", "fixed", "created",
    "calibrated", "tuned", "benchmarked",
    "profiled", "diagnosed"
  ]
}
```

### Adding Categories

When you add custom memory categories (e.g., `people/`, `domain/`), update the routing map:

```json
{
  "routing": {
    "technical": ["implemented", "fixed", "debugged"],
    "project": ["decision", "designed", "architected"],
    "people": ["guest", "preference", "feedback", "user"],
    "domain": ["calibrated", "tuned", "benchmarked"]
  }
}
```

### Disabling Temporarily

Set `"meaningful_keywords": []` in `memory_config.json` to effectively disable the hook without removing it from settings.
