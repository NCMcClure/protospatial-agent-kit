# Loop Prevention and Recovery

Patterns for detecting failure modes and implementing graceful recovery.

## Failure Mode Detection

### The Amnesia Loop

**Symptom:** Agent researches the same file repeatedly across compactions.

**Detection:**
```python
#!/usr/bin/env python3
# scripts/detect_amnesia.py

import json
from collections import Counter

def check_file_access_pattern(log_file: str = ".claude/activity.log") -> dict:
    """Detect repeated file access indicating amnesia loop."""

    with open(log_file) as f:
        entries = [json.loads(line) for line in f]

    file_counts = Counter(e["file"] for e in entries if e.get("file"))

    # Flag if same file accessed 3+ times
    repeated = {f: c for f, c in file_counts.items() if c >= 3}

    if repeated:
        return {
            "detected": True,
            "pattern": "amnesia_loop",
            "files": repeated,
            "recommendation": "Add explicit note about this file to progress.txt"
        }

    return {"detected": False}
```

**Prevention:**
```markdown
# In CLAUDE.md

## Anti-Amnesia Protocol

Before researching any file:
1. Check progress.txt for notes about it
2. If you've looked at it before, read your notes instead
3. If you must re-read, add new findings to progress.txt

Track in progress.txt:
### Files Investigated
- auth.ts: Line 45 has the useEffect issue, needs dependency array fix
- db.js: Connection pool is correct, not the source of the bug
```

### Context Rot

**Symptom:** Reasoning quality degrades after compaction.

**Detection:**
```python
def check_context_health(current_tokens: int, max_tokens: int) -> dict:
    """Check if context is getting dangerously full."""

    usage_pct = current_tokens / max_tokens

    if usage_pct > 0.85:
        return {
            "status": "critical",
            "recommendation": "Use /clear and restart with fresh context"
        }
    elif usage_pct > 0.70:
        return {
            "status": "warning",
            "recommendation": "Use /compact to summarize conversation"
        }

    return {"status": "healthy"}
```

**Prevention: The 30-Minute Rule**

If a session lasts longer than 30 minutes, context likely contains too much garbage. Use `/clear` and start fresh.

### Premature Completion

**Symptom:** Agent declares "Done!" without verification.

**Prevention:** Stop hook that validates claims:

```python
#!/usr/bin/env python3
# scripts/validate_completion.py

import json
import subprocess
import sys

def verify_claimed_features():
    """Check that all features marked 'passes' actually pass tests."""

    with open("feature_list.json") as f:
        features = json.load(f)["features"]

    for feature in features:
        if feature.get("passes"):
            result = subprocess.run(
                ["npm", "test", "--", f"--testNamePattern={feature['id']}"],
                capture_output=True
            )

            if result.returncode != 0:
                return {
                    "decision": "block",
                    "reason": f"Feature {feature['id']} marked passing but tests fail"
                }

    return {"decision": "allow"}

if __name__ == "__main__":
    result = verify_claimed_features()
    print(json.dumps(result))
    sys.exit(0 if result["decision"] == "allow" else 2)
```

### Token Burn

**Symptom:** $100+ spent on an impossible task without progress.

**Prevention:** Iteration limits in loop script:

```bash
#!/bin/bash

MAX_ITERATIONS=50
MAX_COST_DOLLARS=20
ITERATION=0

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    # Check cost if tracking is available
    CURRENT_COST=$(cat .claude/cost.log 2>/dev/null | tail -1 || echo "0")
    if (( $(echo "$CURRENT_COST > $MAX_COST_DOLLARS" | bc -l) )); then
        echo "Cost limit reached: \$$CURRENT_COST"
        exit 1
    fi

    claude --print "$PROMPT"

    ITERATION=$((ITERATION + 1))
done
```

## Circuit Breaker Implementation

### Full Circuit Breaker

```python
#!/usr/bin/env python3
# scripts/circuit_breaker.py
"""Detect stagnation and trigger recovery."""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta

class CircuitBreaker:
    """Monitor loop health and break on stagnation."""

    THRESHOLDS = {
        "no_file_changes": 3,      # consecutive loops without changes
        "same_error": 5,           # same error message repeated
        "output_decrease": 0.7,    # 70% decrease from previous
        "max_duration_minutes": 30 # single session too long
    }

    def __init__(self, state_file: str = ".claude/breaker_state.json"):
        self.state_file = Path(state_file)
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "consecutive_no_change": 0,
            "last_error": None,
            "error_count": 0,
            "last_output_size": 0,
            "session_start": datetime.now().isoformat()
        }

    def _save_state(self):
        self.state_file.parent.mkdir(exist_ok=True)
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def check_file_changes(self) -> bool:
        """Check if files changed since last check."""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        )
        has_changes = bool(result.stdout.strip())

        if not has_changes:
            self.state["consecutive_no_change"] += 1
        else:
            self.state["consecutive_no_change"] = 0

        self._save_state()
        return self.state["consecutive_no_change"] < self.THRESHOLDS["no_file_changes"]

    def check_error_pattern(self, error_msg: str) -> bool:
        """Check if same error is repeating."""
        if error_msg == self.state.get("last_error"):
            self.state["error_count"] += 1
        else:
            self.state["last_error"] = error_msg
            self.state["error_count"] = 1

        self._save_state()
        return self.state["error_count"] < self.THRESHOLDS["same_error"]

    def check_output_health(self, current_size: int) -> bool:
        """Check if output is declining significantly."""
        last_size = self.state.get("last_output_size", current_size)

        if last_size > 0:
            ratio = current_size / last_size
            healthy = ratio > self.THRESHOLDS["output_decrease"]
        else:
            healthy = True

        self.state["last_output_size"] = current_size
        self._save_state()
        return healthy

    def check_duration(self) -> bool:
        """Check if session is running too long."""
        start = datetime.fromisoformat(self.state["session_start"])
        duration = datetime.now() - start
        max_duration = timedelta(minutes=self.THRESHOLDS["max_duration_minutes"])
        return duration < max_duration

    def should_break(self) -> tuple[bool, str]:
        """Check all conditions and return break decision."""

        if not self.check_file_changes():
            return True, "No file changes for 3 consecutive loops"

        if not self.check_duration():
            return True, "Session exceeded 30 minute limit"

        return False, ""

    def reset(self):
        """Reset circuit breaker state."""
        self.state = {
            "consecutive_no_change": 0,
            "last_error": None,
            "error_count": 0,
            "last_output_size": 0,
            "session_start": datetime.now().isoformat()
        }
        self._save_state()


if __name__ == "__main__":
    breaker = CircuitBreaker()
    should_break, reason = breaker.should_break()

    if should_break:
        print(json.dumps({
            "action": "break",
            "reason": reason
        }))
        sys.exit(1)
    else:
        print(json.dumps({"action": "continue"}))
        sys.exit(0)
```

### Integration with Loop Script

```bash
#!/bin/bash
# run_loop.sh with circuit breaker

PROMPT="..."
MAX_ITERATIONS=50
ITERATION=0

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    # Check circuit breaker
    BREAKER_RESULT=$(python3 .claude/scripts/circuit_breaker.py)
    if echo "$BREAKER_RESULT" | grep -q '"action": "break"'; then
        REASON=$(echo "$BREAKER_RESULT" | jq -r '.reason')
        echo "Circuit breaker triggered: $REASON"

        python3 .claude/scripts/circuit_breaker.py --reset

        echo "$REASON" >> .claude/alerts.log

        exit 1
    fi

    claude --print "$PROMPT"

    ITERATION=$((ITERATION + 1))
done
```

## Recovery Strategies

### Strategy 1: Context Reset

When loop is detected, clear and restart with explicit instructions:

```python
def recover_with_context_reset():
    """Clear context and provide explicit re-orientation."""

    with open("progress.txt", "a") as f:
        f.write("\n\n### Recovery: Context Reset\n")
        f.write(f"Time: {datetime.now().isoformat()}\n")
        f.write("Reason: Detected amnesia loop\n")
        f.write("Action: Cleared context, restarting with explicit state\n")

    recovery_prompt = """
    RECOVERY MODE: Previous session detected a loop.

    1. Read progress.txt for full context
    2. Read the "Files Investigated" section carefully
    3. DO NOT re-research files already documented
    4. Continue from the documented "Next Steps"
    """

    return recovery_prompt
```

### Strategy 2: Task Decomposition

When stuck on a complex task, break it down:

```python
def recover_with_decomposition(stuck_feature: str):
    """Break stuck feature into smaller tasks."""

    decomposition_prompt = f"""
    The feature "{stuck_feature}" is too complex.

    1. List 3-5 smaller sub-tasks that comprise this feature
    2. Add each sub-task to feature_list.json as separate items
    3. Mark the original feature as "decomposed: true"
    4. Work on the first sub-task only
    """

    return decomposition_prompt
```

### Strategy 3: Skip and Document

When truly stuck, move on:

```python
def recover_with_skip(blocked_feature: str, reason: str):
    """Skip blocked feature and document for human review."""

    with open("feature_list.json", "r+") as f:
        data = json.load(f)
        for feature in data["features"]:
            if feature["id"] == blocked_feature:
                feature["blocked"] = True
                feature["block_reason"] = reason
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

    with open("progress.txt", "a") as f:
        f.write(f"\n### BLOCKED: {blocked_feature}\n")
        f.write(f"Reason: {reason}\n")
        f.write("Status: Skipped, needs human review\n")

    return "Feature marked as blocked. Moving to next available task."
```

## Checkpoint and Rollback

### Automatic Checkpointing

```python
#!/usr/bin/env python3
# scripts/checkpoint.py
"""Create checkpoint before risky operations."""

import subprocess
from datetime import datetime

def create_checkpoint(name: str = None):
    """Create a git checkpoint."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_name = name or f"checkpoint_{timestamp}"

    subprocess.run(["git", "stash", "push", "-m", checkpoint_name])
    subprocess.run(["git", "tag", f"cp_{checkpoint_name}"])
    subprocess.run(["git", "stash", "pop"])

    return checkpoint_name

def rollback_to_checkpoint(checkpoint_name: str):
    """Rollback to a checkpoint."""
    subprocess.run(["git", "reset", "--hard", f"cp_{checkpoint_name}"])

    with open("progress.txt", "a") as f:
        f.write(f"\n### Rollback to {checkpoint_name}\n")
        f.write(f"Time: {datetime.now().isoformat()}\n")
```

### Integration with Hooks

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/scripts/checkpoint.py"
      }]
    }]
  }
}
```

## Monitoring and Alerting

### Simple File-Based Alerts

```python
#!/usr/bin/env python3
# scripts/alert.py
"""Simple alerting for autonomous loops."""

import json
from datetime import datetime
from pathlib import Path

ALERT_FILE = Path(".claude/alerts.log")

def send_alert(level: str, message: str):
    """Log an alert."""
    alert = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message
    }

    with open(ALERT_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")

def check_alerts():
    """Check for unresolved alerts."""
    if not ALERT_FILE.exists():
        return []

    with open(ALERT_FILE) as f:
        return [json.loads(line) for line in f]
```

### Loop Script with Monitoring

```bash
#!/bin/bash

log_iteration() {
    echo "{\"iteration\": $ITERATION, \"timestamp\": \"$(date -Iseconds)\"}" >> .claude/iterations.log
}

check_progress() {
    local last_commit=$(git log -1 --format="%H" 2>/dev/null)
    local prev_commit=$(cat .claude/last_commit 2>/dev/null)

    if [ "$last_commit" = "$prev_commit" ]; then
        echo "WARNING: No commits in last iteration"
        return 1
    fi

    echo "$last_commit" > .claude/last_commit
    return 0
}
```
