#!/bin/bash
# Autonomous Loop Runner
#
# This script implements the Ralph Wiggum methodology for extended
# autonomous AI coding sessions. It wraps Claude Code in a while loop,
# allowing the agent to persist progress across context boundaries.
#
# Usage: ./run_loop.sh [options]
#
# Options:
#   --max-iterations N    Maximum loop iterations (default: 50)
#   --max-duration M      Maximum duration in minutes (default: 120)
#   --dangerously-skip    Skip permission prompts (use with caution)
#   --dry-run             Print prompt without executing

set -e

# =============================================================================
# Configuration
# =============================================================================

MAX_ITERATIONS=${MAX_ITERATIONS:-50}
MAX_DURATION_MINUTES=${MAX_DURATION_MINUTES:-120}
STATE_FILE="feature_list.json"
PROGRESS_FILE="progress.txt"
SKIP_PERMISSIONS=false
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --max-duration)
            MAX_DURATION_MINUTES="$2"
            shift 2
            ;;
        --dangerously-skip)
            SKIP_PERMISSIONS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# =============================================================================
# The Prompt
# =============================================================================
# This prompt is sent to Claude at the start of each iteration.
# It should be task-agnostic - specific instructions go in CLAUDE.md

PROMPT=$(cat <<'EOF'
## Autonomous Session Start

Read state files and continue development:

1. **Read State**
   - Check `feature_list.json` for current task status
   - Read `progress.txt` for context from previous sessions
   - Review recent git log for what changed

2. **Select Task**
   - Find ONE incomplete item (passes: false)
   - Verify its dependencies are satisfied
   - Read any notes about previous attempts

3. **Implement**
   - Write code for this single feature
   - Create or update tests
   - Run tests to verify

4. **Verify & Complete**
   - Only mark `passes: true` after ALL tests pass
   - Update progress.txt with:
     - What was accomplished
     - Any decisions made
     - Next steps
   - Commit with descriptive message

5. **Exit or Continue**
   - If more work remains, the loop will restart
   - If all features complete, exit successfully

Remember:
- Work on ONE feature at a time
- Verify before marking complete
- Document everything in progress.txt
EOF
)

# =============================================================================
# Pre-flight Checks
# =============================================================================

check_prerequisites() {
    if [[ ! -f "$STATE_FILE" ]]; then
        echo "ERROR: State file not found: $STATE_FILE"
        echo "Run 'cp assets/templates/feature_list.json .' to create it"
        exit 1
    fi

    if [[ ! -f "$PROGRESS_FILE" ]]; then
        echo "WARNING: Progress file not found, creating empty one"
        echo "# Progress Notes" > "$PROGRESS_FILE"
    fi

    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "ERROR: Not a git repository. Initialize with 'git init'"
        exit 1
    fi

    if ! command -v claude &> /dev/null; then
        echo "ERROR: Claude Code not found. Install from https://code.claude.ai"
        exit 1
    fi
}

# =============================================================================
# Completion Check
# =============================================================================

check_completion() {
    python3 -c "
import json
import sys
with open('$STATE_FILE') as f:
    features = json.load(f).get('features', [])
if all(f.get('passes', False) for f in features):
    sys.exit(0)
else:
    sys.exit(1)
" 2>/dev/null
}

# =============================================================================
# Circuit Breaker
# =============================================================================

BREAKER_STATE=".claude/breaker_state.json"

check_circuit_breaker() {
    if [[ -f "$BREAKER_STATE" ]]; then
        local no_change_count=$(python3 -c "
import json
with open('$BREAKER_STATE') as f:
    print(json.load(f).get('consecutive_no_change', 0))
" 2>/dev/null || echo "0")

        if [[ "$no_change_count" -ge 3 ]]; then
            echo "CIRCUIT BREAKER: No changes for 3 consecutive iterations"
            return 1
        fi
    fi
    return 0
}

update_circuit_breaker() {
    local has_changes=$1
    mkdir -p .claude

    python3 -c "
import json
from pathlib import Path
from datetime import datetime

state_file = Path('$BREAKER_STATE')
if state_file.exists():
    state = json.loads(state_file.read_text())
else:
    state = {'consecutive_no_change': 0, 'session_start': datetime.now().isoformat()}

if $has_changes:
    state['consecutive_no_change'] = 0
else:
    state['consecutive_no_change'] = state.get('consecutive_no_change', 0) + 1

state_file.write_text(json.dumps(state, indent=2))
"
}

# =============================================================================
# Main Loop
# =============================================================================

main() {
    check_prerequisites

    echo "=============================================="
    echo "  Autonomous Loop Runner"
    echo "=============================================="
    echo "State file:      $STATE_FILE"
    echo "Progress file:   $PROGRESS_FILE"
    echo "Max iterations:  $MAX_ITERATIONS"
    echo "Max duration:    $MAX_DURATION_MINUTES minutes"
    echo "Skip permissions: $SKIP_PERMISSIONS"
    echo "=============================================="
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "DRY RUN - Prompt that would be sent:"
        echo "--------------------------------------"
        echo "$PROMPT"
        echo "--------------------------------------"
        exit 0
    fi

    START_TIME=$(date +%s)
    ITERATION=0

    # Reset circuit breaker
    rm -f "$BREAKER_STATE"

    while [[ $ITERATION -lt $MAX_ITERATIONS ]]; do
        echo ""
        echo "=== Iteration $ITERATION / $MAX_ITERATIONS ==="
        echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"

        CURRENT_TIME=$(date +%s)
        DURATION_MINUTES=$(( (CURRENT_TIME - START_TIME) / 60 ))
        echo "Duration: $DURATION_MINUTES / $MAX_DURATION_MINUTES minutes"

        if [[ $DURATION_MINUTES -ge $MAX_DURATION_MINUTES ]]; then
            echo ""
            echo "Duration limit reached. Stopping."
            break
        fi

        if check_completion; then
            echo ""
            echo "All features complete!"
            exit 0
        fi

        if ! check_circuit_breaker; then
            echo "Circuit breaker triggered. Stopping to prevent waste."
            break
        fi

        GIT_STATUS_BEFORE=$(git status --porcelain 2>/dev/null || echo "")
        GIT_HEAD_BEFORE=$(git rev-parse HEAD 2>/dev/null || echo "")

        CLAUDE_CMD="claude --print"
        if [[ "$SKIP_PERMISSIONS" == "true" ]]; then
            CLAUDE_CMD="$CLAUDE_CMD --dangerously-skip-permissions"
        fi

        echo "Running Claude..."
        $CLAUDE_CMD "$PROMPT"
        EXIT_CODE=$?

        if [[ $EXIT_CODE -ne 0 ]]; then
            echo "Claude exited with code: $EXIT_CODE"
        fi

        GIT_STATUS_AFTER=$(git status --porcelain 2>/dev/null || echo "")
        GIT_HEAD_AFTER=$(git rev-parse HEAD 2>/dev/null || echo "")

        if [[ "$GIT_STATUS_BEFORE" != "$GIT_STATUS_AFTER" ]] || \
           [[ "$GIT_HEAD_BEFORE" != "$GIT_HEAD_AFTER" ]]; then
            update_circuit_breaker "True"
            echo "Changes detected in this iteration"
        else
            update_circuit_breaker "False"
            echo "No changes in this iteration"
        fi

        ITERATION=$((ITERATION + 1))
    done

    echo ""
    echo "=============================================="
    echo "Loop ended after $ITERATION iterations"
    echo "Total duration: $DURATION_MINUTES minutes"
    echo "=============================================="

    if check_completion; then
        echo "Status: COMPLETE"
        exit 0
    else
        echo "Status: INCOMPLETE (stopped by limit)"
        exit 1
    fi
}

main "$@"
