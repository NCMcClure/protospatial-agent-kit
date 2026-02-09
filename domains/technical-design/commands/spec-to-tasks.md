Break a technical specification into an ordered implementation task list.

Take a spec (provided by the user, or output from /design-to-spec) and decompose it into discrete, actionable implementation tasks.

For each task, provide:
1. **Task name** — imperative verb phrase ("Implement panel entrance animation", not "Panel animation")
2. **Description** — what specifically needs to be done
3. **Dependencies** — which other tasks must complete first (by task number)
4. **Complexity** — S (hours), M (day), L (days)
5. **Needs design review** — flag tasks where implementation choices need designer sign-off before proceeding

Ordering rules:
- Foundation tasks first (data models, interfaces, base classes)
- Core behavior before edge cases
- Interaction logic before visual polish
- Parallelizable tasks grouped together and marked as such

Output format:

```
## Task Breakdown: [Feature Name]

### Phase 1: Foundation
1. [Task] — [S/M/L] — [Description]
2. [Task] — [S/M/L] — [Description] (depends on: 1)

### Phase 2: Core Behavior
3. [Task] — [S/M/L] — [Description] (depends on: 1, 2)
   ⚠️ Needs design review: [specific question]

### Phase 3: Polish & Edge Cases (parallelizable)
4. [Task] — [S/M/L] — [Description] (depends on: 3)
5. [Task] — [S/M/L] — [Description] (depends on: 3)
```

$ARGUMENTS
