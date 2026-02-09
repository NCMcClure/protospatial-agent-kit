# Project: [Name]

## Overview
[One paragraph describing the project]

## Tech Stack
- Language: [e.g., TypeScript]
- Runtime: [e.g., Node.js 20]
- Framework: [e.g., Express.js]
- Database: [e.g., PostgreSQL]
- Testing: [e.g., Jest]

## Commands
```
npm run dev      # Development server
npm test         # Run tests
npm run lint     # Lint code
npm run build    # Production build
```

## Architecture
Key directories:
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation

See `docs/architecture.md` for detailed design.

---

## Autonomous Loop Protocol

IMPORTANT: When running in autonomous mode, follow this protocol exactly.

### 1. Session Start
- Read `feature_list.json` for task status
- Read `progress.txt` for previous session context
- Check recent git commits

### 2. Task Selection
- Pick ONE incomplete feature (passes: false)
- Check dependencies are satisfied
- Read any notes from previous attempts

### 3. Implementation
- Work incrementally
- Commit logical chunks
- Run tests frequently

### 4. Verification
Before marking any feature as `passes: true`:
- Run full test suite: `npm test`
- Verify related tests pass
- Manual smoke test if applicable

### 5. Session End
- Update `feature_list.json` (only after verification)
- Add detailed notes to `progress.txt`:
  - What was accomplished
  - Any blockers
  - Decisions made
  - Next steps
- Commit with format: `feat(scope): description`

---

## Constraints

YOU MUST:
- Read progress.txt before starting work
- Run tests before marking features complete
- Document blockers in progress.txt
- Commit after each completed feature

YOU MUST NOT:
- Mark features passing without test verification
- Work on multiple features simultaneously
- Skip reading previous session notes
- Make changes without committing

---

## Context Management

If context reaches 70%:
- Use `/compact` to summarize
- Update progress.txt with current state

If stuck for 3+ attempts on same issue:
- Document the blocker in progress.txt
- Move to next task or request human review

Use `/clear` between unrelated tasks.

---

## Session Notes

<!-- Auto-updated by sessions -->
### Latest: [Date]
- Completed:
- In Progress:
- Next:
