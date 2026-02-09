---
name: autonomous-loop
description: >
  Create task-specific autonomous agentic coding loop skills using the Ralph
  Wiggum methodology. Use when building harnesses for Claude Code to run
  autonomously for extended periods, implementing iterative development loops,
  creating self-healing agent pipelines, or designing systems where AI agents
  persist through context window boundaries. Triggers include requests for
  "autonomous coding", "agentic loops", "Ralph Wiggum", "self-running agents",
  "iterative AI development", "continuous coding loops", or "headless Claude Code".
---

# Autonomous Agentic Loop Skill Creator

Create task-specific skills that enable Claude Code to run autonomously for hours, persisting state across context windows and recovering from failures gracefully.

## Core Concept

The Ralph Wiggum Loop externalizes agent memory to the filesystem. A bash while loop continuously invokes Claude Code with the same prompt. Progress persists in files and git — not in the context window. When context fills, a fresh instance continues by reading filesystem state.

```
┌─────────────────────────────────────────────────────────┐
│                    OUTER LOOP (bash)                    │
│  while true; do claude --print "$PROMPT"; done          │
└─────────────────────────────────────────────────────────┘
         │                                    ▲
         ▼                                    │
┌─────────────────────────────────────────────────────────┐
│              CLAUDE CODE SESSION                        │
│  1. Read state files (feature_list.json, progress.txt)  │
│  2. Pick ONE task                                       │
│  3. Implement → Test → Verify                           │
│  4. Update state files                                  │
│  5. Git commit                                          │
│  6. Exit (Stop hook validates completion)               │
└─────────────────────────────────────────────────────────┘
         │                                    ▲
         ▼                                    │
┌─────────────────────────────────────────────────────────┐
│                 PERSISTENT STATE                        │
│  • feature_list.json  - Task tracking (pass/fail)       │
│  • progress.txt       - Session handoff notes           │
│  • .claude/hooks/     - Validation & control            │
│  • Git history        - Rollback capability             │
└─────────────────────────────────────────────────────────┘
```

## Creating a Task-Specific Loop Skill

### Step 1: Define the Goal Structure

Determine what "done" means for your autonomous task:

| Goal Type | State File Format | Example |
|-----------|-------------------|---------|
| Feature list | JSON with `passes: boolean` | Building an app feature-by-feature |
| Checklist | Markdown with `- [x]` items | Migration or refactoring tasks |
| Test suite | JSON with test results | Test-driven development |
| Spec compliance | JSON with requirement IDs | Implementing a specification |

### Step 2: Design State Files

Create state files that survive context boundaries. Use JSON for structured data (prevents accidental description edits):

```json
// feature_list.json - The agent can ONLY change "passes" field
{
  "features": [
    {"id": "auth-001", "name": "User login", "passes": false},
    {"id": "auth-002", "name": "Password reset", "passes": false}
  ]
}
```

```text
# progress.txt - Human-readable session notes
## Last Session: 2025-02-04 14:30
- Completed: auth-001 (user login)
- Current: auth-002 (password reset) - blocked on email service
- Next: auth-003 (session management)
- Constraints: Using bcrypt, no plaintext passwords
```

### Step 3: Configure Hooks

Hooks control agent behavior at lifecycle points. See [references/hooks-reference.md](references/hooks-reference.md) for complete patterns.

**Essential hooks for autonomous loops:**

1. **Stop hook** - Prevents premature exit until completion criteria met
2. **PostToolUse hook** - Auto-format, auto-test after edits
3. **PreToolUse hook** - Block dangerous operations

Minimal Stop hook for feature-list validation:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python3 scripts/validate_completion.py"
      }]
    }]
  }
}
```

### Step 4: Create the Loop Script

```bash
#!/bin/bash
# run_loop.sh - The outer autonomous loop

PROMPT=$(cat <<'EOF'
Read feature_list.json and progress.txt.
Pick ONE incomplete feature (passes: false).
Implement it fully with tests.
Run tests to verify.
Only mark passes: true after ALL tests pass.
Update progress.txt with session notes.
Commit with descriptive message.
EOF
)

# Safety limits
MAX_ITERATIONS=50
ITERATION=0

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    echo "=== Iteration $ITERATION ==="

    # Check if all features complete
    if python3 -c "import json; f=json.load(open('feature_list.json')); exit(0 if all(x['passes'] for x in f['features']) else 1)"; then
        echo "All features complete!"
        exit 0
    fi

    # Run Claude Code
    claude --print --dangerously-skip-permissions "$PROMPT"
    EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "Claude exited with error: $EXIT_CODE"
    fi

    ITERATION=$((ITERATION + 1))
done

echo "Reached max iterations"
```

### Step 5: Implement Validation Scripts

```python
#!/usr/bin/env python3
"""Stop hook validator - blocks exit until criteria met."""

import json
import subprocess
import sys

def check_tests_pass():
    """Run test suite, return True if all pass."""
    result = subprocess.run(
        ["npm", "test", "--", "--passWithNoTests"],
        capture_output=True, text=True
    )
    return result.returncode == 0

def check_feature_verified():
    """Ensure recently modified feature was tested."""
    with open("feature_list.json") as f:
        features = json.load(f)["features"]

    passing = [f for f in features if f["passes"]]
    if not passing:
        return True  # No claims to verify yet

    latest = passing[-1]
    # Add your verification logic here
    return True

def main():
    result = {"decision": "allow"}

    if not check_tests_pass():
        result = {
            "decision": "block",
            "reason": "Tests failing. Fix before continuing."
        }
    elif not check_feature_verified():
        result = {
            "decision": "block",
            "reason": "Feature marked passing but not verified."
        }

    print(json.dumps(result))
    return 0 if result["decision"] == "allow" else 2

if __name__ == "__main__":
    sys.exit(main())
```

## Skill Structure for Your Task

When creating a task-specific loop skill, organize as:

```
my-loop-skill/
├── SKILL.md              # Task-specific instructions
├── scripts/
│   ├── run_loop.sh       # Outer loop script
│   ├── validate_completion.py
│   └── circuit_breaker.py
├── references/
│   └── task-details.md   # Domain-specific guidance
└── assets/
    └── templates/
        ├── feature_list.json
        ├── progress.txt
        └── hooks.json
```

## Critical Patterns

### Preventing Failure Modes

| Failure Mode | Symptom | Prevention |
|--------------|---------|------------|
| Amnesia Loop | Same file researched repeatedly | Track visited files in progress.txt |
| Premature Completion | "Done!" without verification | Stop hook validates all tests pass |
| Context Rot | Degraded reasoning after compaction | Clear context every 30 min or at 70% |
| Token Burn | $100+ on impossible task | MAX_ITERATIONS limit in loop script |

### The Initializer Pattern

For complex projects, use two-phase approach:

1. **Initializer session** (run once):
   - Create feature_list.json with all requirements
   - Write init.sh for dev server setup
   - Create initial progress.txt
   - Make baseline git commit

2. **Coding sessions** (run in loop):
   - Read state files
   - Work on ONE feature
   - Verify before marking complete
   - Commit and update notes

### Circuit Breaker Implementation

See [references/loop-prevention.md](references/loop-prevention.md) for complete patterns.

```python
# circuit_breaker.py - Detect stagnation
STAGNATION_SIGNALS = {
    "no_file_changes": 3,      # consecutive loops
    "same_error": 5,           # consecutive occurrences
    "output_decrease": 0.7,    # 70% drop from previous
}
```

## CLAUDE.md Configuration

Keep under 300 lines. Include only:

```markdown
# Project: [Name]

## Tech Stack
- [List technologies]

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Autonomous Loop Protocol
1. Read feature_list.json and progress.txt first
2. Work on ONE feature per session
3. Run tests before marking complete
4. Update progress.txt before exiting
5. Commit with format: `feat(scope): description`

## IMPORTANT
- Never mark passes: true without verified tests
- If stuck for 3 attempts, document blocker and move on
- Check progress.txt for constraints from previous sessions
```

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| Loop script | Outer while loop | `scripts/run_loop.sh` |
| Stop hook | Prevent premature exit | `.claude/hooks.json` |
| Feature list | Track progress | `feature_list.json` |
| Progress notes | Session handoff | `progress.txt` |
| Circuit breaker | Detect stagnation | `scripts/circuit_breaker.py` |

## Additional References

- [Hooks Reference](references/hooks-reference.md) - Complete hook patterns
- [CLAUDE.md Patterns](references/claude-md-patterns.md) - Configuration best practices
- [MCP Patterns](references/mcp-patterns.md) - Tool integration strategies
- [Loop Prevention](references/loop-prevention.md) - Circuit breakers and recovery

## Initialization

Use the initialization script to scaffold a new task-specific loop skill:

```bash
python3 scripts/init_loop_skill.py <skill-name> --goal-type feature-list
```

Options for `--goal-type`: `feature-list`, `checklist`, `test-suite`, `spec-compliance`
