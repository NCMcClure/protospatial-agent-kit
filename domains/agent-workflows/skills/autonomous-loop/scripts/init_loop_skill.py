#!/usr/bin/env python3
"""Initialize a new task-specific autonomous loop skill.

Usage:
    python3 init_loop_skill.py <skill-name> --goal-type <type> [--output-dir <dir>]

Goal types:
    feature-list    - JSON feature list with pass/fail tracking
    checklist       - Markdown checklist with [x] items
    test-suite      - Test-driven development with test results
    spec-compliance - Specification requirement tracking
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

TEMPLATES = {
    "feature-list": {
        "state_file": "feature_list.json",
        "state_content": {
            "metadata": {
                "created": "",
                "description": "Feature tracking for autonomous development",
                "version": "1.0"
            },
            "features": [
                {"id": "example-001", "name": "Example feature", "passes": False, "notes": ""},
            ]
        },
        "completion_check": '''
def check_completion():
    """Return True if all features pass."""
    import json
    with open("feature_list.json") as f:
        features = json.load(f)["features"]
    return all(f.get("passes", False) for f in features)
'''
    },
    "checklist": {
        "state_file": "checklist.md",
        "state_content": """# Task Checklist

## In Progress
- [ ] Example task 1
- [ ] Example task 2
- [ ] Example task 3

## Completed
<!-- Move completed items here -->

## Blocked
<!-- Document blockers here -->
""",
        "completion_check": '''
def check_completion():
    """Return True if no unchecked items remain."""
    with open("checklist.md") as f:
        content = f.read()
    return "- [ ]" not in content
'''
    },
    "test-suite": {
        "state_file": "test_status.json",
        "state_content": {
            "metadata": {
                "created": "",
                "test_command": "npm test -- --json",
                "version": "1.0"
            },
            "suites": [
                {"name": "example.test.js", "status": "pending", "last_run": None}
            ]
        },
        "completion_check": '''
def check_completion():
    """Return True if all test suites pass."""
    import json
    with open("test_status.json") as f:
        suites = json.load(f)["suites"]
    return all(s.get("status") == "pass" for s in suites)
'''
    },
    "spec-compliance": {
        "state_file": "spec_requirements.json",
        "state_content": {
            "metadata": {
                "created": "",
                "spec_document": "docs/specification.md",
                "version": "1.0"
            },
            "requirements": [
                {"id": "REQ-001", "description": "Example requirement", "implemented": False, "verified": False}
            ]
        },
        "completion_check": '''
def check_completion():
    """Return True if all requirements are implemented and verified."""
    import json
    with open("spec_requirements.json") as f:
        reqs = json.load(f)["requirements"]
    return all(r.get("implemented") and r.get("verified") for r in reqs)
'''
    }
}


def create_skill_structure(skill_name: str, goal_type: str, output_dir: Path):
    """Create the skill directory structure."""

    skill_dir = output_dir / skill_name

    # Create directories
    (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets" / "templates").mkdir(parents=True, exist_ok=True)

    template = TEMPLATES[goal_type]

    # Create SKILL.md
    skill_md = f'''---
name: {skill_name}
description: >
  Autonomous agentic loop for {skill_name.replace("-", " ")}.
  Implements the Ralph Wiggum methodology with {goal_type} tracking.
---

# {skill_name.replace("-", " ").title()}

Autonomous loop skill for [describe your task domain].

## Quick Start

1. Initialize state:
   ```bash
   cp assets/templates/{template["state_file"]} .
   cp assets/templates/progress.txt .
   ```

2. Configure hooks (copy hooks.json to .claude/settings.json)

3. Run the loop:
   ```bash
   ./scripts/run_loop.sh
   ```

## State Management

This skill uses `{template["state_file"]}` for tracking progress.

### Reading State
Always read state files at the start of each session:
1. Check `{template["state_file"]}` for current task status
2. Read `progress.txt` for context from previous sessions

### Updating State
After completing work:
1. Update `{template["state_file"]}` only after verification
2. Add notes to `progress.txt`
3. Commit changes

## Verification Protocol

Before marking any item as complete:
1. Run tests: [your test command]
2. Verify manually if applicable
3. Update state file
4. Commit with descriptive message

## Customization

Edit these files for your specific needs:
- `scripts/run_loop.sh` - Loop configuration and limits
- `scripts/validate_completion.py` - Completion criteria
- `assets/templates/hooks.json` - Hook behavior

## References

- See `references/task-guide.md` for domain-specific guidance
'''

    (skill_dir / "SKILL.md").write_text(skill_md)

    # Create run_loop.sh
    run_loop = f'''#!/bin/bash
# Autonomous loop runner for {skill_name}

set -e

MAX_ITERATIONS=${{MAX_ITERATIONS:-50}}
MAX_DURATION_MINUTES=${{MAX_DURATION_MINUTES:-120}}
STATE_FILE="{template["state_file"]}"

PROMPT=$(cat <<'EOF'
Read {template["state_file"]} and progress.txt.
Identify the next incomplete item.
Implement it fully with proper testing.
Verify before marking complete.
Update progress.txt with session notes.
Commit with a descriptive message.
EOF
)

START_TIME=$(date +%s)
ITERATION=0

echo "Starting autonomous loop for {skill_name}"
echo "Max iterations: $MAX_ITERATIONS"

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    echo ""
    echo "=== Iteration $ITERATION ==="

    CURRENT_TIME=$(date +%s)
    DURATION=$(( (CURRENT_TIME - START_TIME) / 60 ))
    if [ $DURATION -ge $MAX_DURATION_MINUTES ]; then
        echo "Duration limit reached: $DURATION minutes"
        break
    fi

    if python3 scripts/check_completion.py; then
        echo "All tasks complete!"
        exit 0
    fi

    claude --print --dangerously-skip-permissions "$PROMPT"

    ITERATION=$((ITERATION + 1))
done

echo "Loop ended after $ITERATION iterations"
'''

    run_loop_path = skill_dir / "scripts" / "run_loop.sh"
    run_loop_path.write_text(run_loop)
    os.chmod(run_loop_path, 0o755)

    # Create check_completion.py
    check_completion = f'''#!/usr/bin/env python3
"""Check if all tasks are complete."""

import sys

{template["completion_check"]}

if __name__ == "__main__":
    if check_completion():
        print("All tasks complete")
        sys.exit(0)
    else:
        print("Tasks remaining")
        sys.exit(1)
'''

    (skill_dir / "scripts" / "check_completion.py").write_text(check_completion)

    # Create template state file
    state_content = template["state_content"]
    if isinstance(state_content, dict):
        state_content["metadata"]["created"] = datetime.now().isoformat()
        content = json.dumps(state_content, indent=2)
    else:
        content = state_content

    (skill_dir / "assets" / "templates" / template["state_file"]).write_text(content)

    # Create progress.txt template
    progress_template = f'''# Progress Notes

## Project: {skill_name.replace("-", " ").title()}
## Created: {datetime.now().strftime("%Y-%m-%d")}

---

## Session Notes

### Current Session
- Started:
- Working on:
- Completed:
- Blocked:
- Next:

---

## Files Investigated
<!-- Track files you've looked at to prevent amnesia loops -->

---

## Decisions Made
<!-- Document important decisions and their rationale -->

---

## Constraints
<!-- List any constraints discovered during development -->
'''

    (skill_dir / "assets" / "templates" / "progress.txt").write_text(progress_template)

    # Create hooks.json template
    hooks_json = {
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

    (skill_dir / "assets" / "templates" / "hooks.json").write_text(json.dumps(hooks_json, indent=2))

    # Create task-guide.md reference
    task_guide = f'''# Task Guide for {skill_name.replace("-", " ").title()}

## Overview

[Describe the specific task domain this skill handles]

## State File Format

This skill uses `{template["state_file"]}` for tracking.

[Document the state file structure and how to update it]

## Verification Requirements

Before marking any item complete:

1. [Specific verification step 1]
2. [Specific verification step 2]
3. [Specific verification step 3]

## Common Issues

[Document common issues and solutions as they arise]

## Domain-Specific Constraints

[List any constraints specific to this task domain]
'''

    (skill_dir / "references" / "task-guide.md").write_text(task_guide)

    print(f"Created skill: {skill_dir}")
    print(f"")
    print(f"Next steps:")
    print(f"  1. Edit {skill_dir}/SKILL.md with your task-specific instructions")
    print(f"  2. Customize {skill_dir}/assets/templates/{template['state_file']}")
    print(f"  3. Add domain knowledge to {skill_dir}/references/task-guide.md")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new autonomous loop skill"
    )
    parser.add_argument("skill_name", help="Name of the skill (e.g., 'webapp-builder')")
    parser.add_argument(
        "--goal-type",
        choices=list(TEMPLATES.keys()),
        default="feature-list",
        help="Type of goal tracking to use"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for the skill"
    )

    args = parser.parse_args()

    create_skill_structure(args.skill_name, args.goal_type, args.output_dir)


if __name__ == "__main__":
    main()
