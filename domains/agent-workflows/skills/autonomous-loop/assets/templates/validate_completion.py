#!/usr/bin/env python3
"""
Stop Hook Validator for Autonomous Loops

This script is called by the Stop hook to validate that the session
should be allowed to end. It prevents premature completion by verifying
that claimed work is actually done.

Exit codes:
- 0: Allow exit (all validations pass)
- 2: Block exit (validation failed, stderr shown to Claude)

Output:
- JSON object with 'decision' field ('allow' or 'block')
- If blocking, include 'reason' field

Usage:
    Called automatically by .claude/hooks.json Stop hook
    Can also be run manually: python3 validate_completion.py
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Tuple

# =============================================================================
# Configuration
# =============================================================================

STATE_FILE = Path("feature_list.json")
PROGRESS_FILE = Path("progress.txt")
TEST_COMMAND = ["npm", "test", "--", "--passWithNoTests"]

# =============================================================================
# Validation Functions
# =============================================================================

def check_tests_pass() -> Tuple[bool, str]:
    """Run test suite and verify all tests pass."""
    try:
        result = subprocess.run(
            TEST_COMMAND,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            return True, "Tests passing"
        else:
            stderr = result.stderr[-500:] if result.stderr else ""
            stdout = result.stdout[-500:] if result.stdout else ""
            return False, f"Tests failing:\n{stdout}\n{stderr}"

    except subprocess.TimeoutExpired:
        return False, "Test suite timed out"
    except FileNotFoundError:
        # npm not found, skip test check
        return True, "Test command not available, skipping"


def check_state_file_valid() -> Tuple[bool, str]:
    """Verify state file exists and is valid JSON."""
    if not STATE_FILE.exists():
        return False, f"State file not found: {STATE_FILE}"

    try:
        with open(STATE_FILE) as f:
            data = json.load(f)

        if "features" not in data:
            return False, "State file missing 'features' key"

        return True, "State file valid"

    except json.JSONDecodeError as e:
        return False, f"State file is invalid JSON: {e}"


def check_no_uncommitted_changes() -> Tuple[bool, str]:
    """Verify all changes are committed."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            files = result.stdout.strip().split('\n')[:5]
            return False, f"Uncommitted changes:\n" + "\n".join(files)

        return True, "All changes committed"

    except FileNotFoundError:
        return True, "Git not available, skipping"


def check_progress_updated() -> Tuple[bool, str]:
    """Verify progress.txt was updated in this session."""
    if not PROGRESS_FILE.exists():
        return False, "Progress file not found"

    try:
        import time
        mtime = PROGRESS_FILE.stat().st_mtime
        age_minutes = (time.time() - mtime) / 60

        if age_minutes > 60:
            return False, "Progress file not updated recently"

        return True, "Progress file updated"

    except Exception as e:
        return True, f"Could not check progress file age: {e}"


def check_feature_verification() -> Tuple[bool, str]:
    """Verify features marked as passing have evidence of verification."""
    try:
        with open(STATE_FILE) as f:
            data = json.load(f)

        features = data.get("features", [])
        passing = [f for f in features if f.get("passes")]

        for feature in passing:
            feature_id = feature.get("id", "unknown")

            test_patterns = [
                f"tests/{feature_id}.test.js",
                f"tests/{feature_id}.test.ts",
                f"test/{feature_id}.test.js",
                f"__tests__/{feature_id}.test.js",
            ]

            has_test = any(Path(p).exists() for p in test_patterns)

            if not has_test and not feature.get("notes"):
                return False, f"Feature {feature_id} marked passing but no test or notes"

        return True, "All passing features verified"

    except Exception as e:
        return True, f"Could not check feature verification: {e}"


# =============================================================================
# Main Validation Logic
# =============================================================================

def run_validations() -> dict:
    """Run all validations and return result."""

    validations = [
        ("State file valid", check_state_file_valid),
        ("Tests passing", check_tests_pass),
        ("Changes committed", check_no_uncommitted_changes),
        ("Progress updated", check_progress_updated),
        ("Features verified", check_feature_verification),
    ]

    failed = []

    for name, check_fn in validations:
        try:
            passed, message = check_fn()
            if not passed:
                failed.append(f"{name}: {message}")
        except Exception as e:
            print(f"Warning: {name} check failed with error: {e}", file=sys.stderr)

    if failed:
        return {
            "decision": "block",
            "reason": "Validation failed:\n" + "\n".join(failed)
        }

    return {"decision": "allow"}


def main():
    """Entry point for Stop hook."""

    result = run_validations()

    print(json.dumps(result))

    if result["decision"] == "allow":
        return 0
    else:
        print(f"BLOCKED: {result.get('reason', 'Unknown')}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
