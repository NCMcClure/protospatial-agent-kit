# CLAUDE.md Patterns for Autonomous Loops

Best practices for configuring CLAUDE.md to support extended autonomous operation.

## Core Principles

1. **Under 300 lines** - Longer files get ignored
2. **No code snippets** - They become outdated; use file:line references
3. **Use formatters** - Don't write style guides, enforce with tools
4. **Progressive disclosure** - Point to reference files, don't duplicate

## Hierarchical Loading

```
~/.claude/CLAUDE.md          # Personal settings (all projects)
./CLAUDE.md                   # Team settings (commit to git)
./CLAUDE.local.md            # Personal overrides (in .gitignore)
./src/CLAUDE.md              # Subdirectory context (loaded on-demand)
```

## Template: Autonomous Loop Project

```markdown
# Project: [Name]

## Overview
[One paragraph describing the project and its purpose]

## Tech Stack
- Runtime: Node.js 20
- Framework: Express.js
- Database: PostgreSQL
- Testing: Jest

## Commands
npm run dev      # Start development server
npm test         # Run all tests
npm run lint     # Run ESLint
npm run build    # Production build

## Architecture
See `docs/architecture.md` for detailed design.
Key directories:
- `src/api/` - REST endpoints
- `src/services/` - Business logic
- `src/models/` - Database models

## Autonomous Loop Protocol

IMPORTANT: When running in autonomous mode:

1. **Always read state first**
   - Check `feature_list.json` for current task status
   - Read `progress.txt` for context from previous sessions
   - Review recent git commits for what was changed

2. **Work incrementally**
   - Pick ONE feature/task per session
   - Implement completely before moving on
   - Never start multiple features simultaneously

3. **Verify before marking complete**
   - Run tests: `npm test -- --testPathPattern="<feature>"`
   - Check lint: `npm run lint`
   - Manual smoke test if applicable

4. **Update state before exiting**
   - Update `feature_list.json` only after verification
   - Add notes to `progress.txt` about:
     - What was accomplished
     - Any blockers encountered
     - Decisions made and why
     - Next steps

5. **Commit with context**
   - Format: `feat(scope): description`
   - Include "why" in commit body
   - Reference feature ID

## Constraints

YOU MUST:
- Run tests before marking any feature as passing
- Document blockers in progress.txt if stuck
- Commit after each completed feature

YOU MUST NOT:
- Mark features passing without test verification
- Skip reading progress.txt at session start
- Make changes without committing
```

## Template: Test-Driven Loop

```markdown
# Project: [Name]

## Test-First Protocol

When running autonomously:

1. **Read test specification**
   - Check `specs/` for feature requirements
   - Read existing tests in `tests/`

2. **Write test first**
   - Create failing test for the feature
   - Commit: `test(scope): add tests for <feature>`

3. **Implement to pass**
   - Write minimal code to pass test
   - Commit: `feat(scope): implement <feature>`

4. **Refactor if needed**
   - Clean up implementation
   - Ensure tests still pass
   - Commit: `refactor(scope): clean up <feature>`

5. **Update tracking**
   - Mark feature as passing in feature_list.json
   - Add notes to progress.txt
```

## Template: Migration/Refactoring Loop

```markdown
# Project: [Name]

## Migration Protocol

Working through `migration_checklist.md`:

1. **Check current item**
   - Find first unchecked `- [ ]` item
   - Read any notes about it

2. **Create safety net**
   - Ensure tests cover affected code
   - Create checkpoint: `git stash push -m "pre-migration"`

3. **Execute migration**
   - Make the change
   - Run tests immediately
   - If tests fail, restore: `git stash pop`

4. **Verify and document**
   - Mark `- [x]` in checklist
   - Add migration notes
   - Commit with `migrate(scope): <item>`

5. **Continue or pause**
   - If errors persist, document in progress.txt
   - Move to next item or pause for human review
```

## Anti-Patterns to Avoid

### Don't: Over-specify Code Style

```markdown
## Code Style
- Use 2 spaces for indentation
- Use single quotes for strings
- Add trailing commas
... (50 more rules)
```

### Do: Delegate to Tools

```markdown
## Code Style
Enforced by ESLint and Prettier. Run `npm run lint:fix` to auto-format.
```

### Don't: Embed Code Blocks

```markdown
## Database Connection
Use this exact code:
const { Pool } = require('pg');
const pool = new Pool({ ... });
```

### Do: Reference Files

```markdown
## Database
Connection configured in `src/db/pool.js`.
Environment variables documented in `.env.example`.
```

### Don't: Duplicate Documentation

```markdown
## API Reference
### GET /users
Returns list of users...
(repeating what's in OpenAPI spec)
```

### Do: Point to Source of Truth

```markdown
## API
OpenAPI spec: `docs/openapi.yaml`
Generate docs: `npm run docs`
```

## Context Management Commands

Include these reminders for autonomous operation:

```markdown
## Context Management

If context window reaches 70%:
- Use `/compact` to summarize conversation
- Update progress.txt with current state
- Continue with fresh context

If stuck for 3+ attempts:
- Document blocker in progress.txt
- Commit current progress
- Move to next task or pause

Use `/clear` between unrelated tasks.
```

## Feature Flags for Behavior

```markdown
## Autonomous Behavior Flags

Set in progress.txt header:
- `STRICT_VERIFICATION: true` - Block commits without tests
- `AUTO_FORMAT: true` - Run prettier after edits
- `PAUSE_ON_ERROR: true` - Stop loop on first error
- `VERBOSE_LOGGING: true` - Detailed progress notes
```

## Session Handoff Section

Always include space for session notes:

```markdown
## Session Notes

<!-- Updated by autonomous sessions -->
### Latest Session
- Date:
- Completed:
- In Progress:
- Blocked:
- Next:
```

## Imports with @syntax

For modular configuration:

```markdown
# CLAUDE.md

@.claude/project-context.md
@.claude/loop-protocol.md
@.claude/constraints.md
```

Maximum import depth: 5 levels. Keep flat when possible.
