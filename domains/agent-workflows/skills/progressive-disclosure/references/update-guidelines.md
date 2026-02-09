# Memory Update Guidelines

Rules for maintaining memory freshness, deciding when to update vs archive, and ensuring every memory file earns its place in the system.

## The Two-Reader Test

Before writing anything to memory, apply this test:

**Will this be useful to a future Claude session working on this project?**
AND/OR
**Will this be useful to the human reviewing project knowledge?**

If yes to either → capture it.
If no to both → don't capture it. It's noise.

Examples that pass:
- "The WebSocket reconnection logic requires a 3-second backoff because the server rate-limits at 2 reconnections/second" → yes, future sessions need this
- "We chose PostgreSQL over MongoDB because our data is relational and we need ACID transactions" → yes, the human needs to remember why
- "The BPM analysis script takes 4 minutes for 3,000 tracks; pre-cache results" → yes, avoids re-discovery

Examples that fail:
- "Spent 20 minutes debugging a typo in the config file" → no future value
- "Ran npm install" → ephemeral, not knowledge
- "Claude suggested approach X but we went with Y" → unless you record WHY Y was better, this is noise

## When to Update vs When to Create

**Update an existing file** when:
- New information extends or corrects what's already there
- The Quick Summary needs to reflect current reality
- A decision has been reversed or refined
- New learnings relate to the same topic the file covers

**Create a new file** when:
- The topic doesn't fit any existing file's scope
- An existing file would exceed 200 lines by adding this content (split instead)
- A new category of knowledge has emerged that warrants its own file

**Never** create a new file for information that fits naturally in an existing file. One well-maintained file with 150 lines is better than three 50-line files that fragment the same topic.

## Timestamp Convention

Add timestamps to significant updates so readers can assess freshness:

```markdown
## Architecture Decisions

### API Gateway Pattern (2025-01)
Chose Kong over custom middleware because...

### Database Migration Strategy (2025-03)
Switched from Flyway to Liquibase after discovering...

### Cache Layer Addition (2025-06)
Added Redis caching for the product catalog endpoint...
```

The timestamp format is `YYYY-MM` for decisions and milestones, `YYYY-MM-DD` when precision matters (incident records, specific debugging sessions).

Timestamps go in section headers or inline, not in the filename. Files are named for their topic, not their date.

## Quick Summary Maintenance

The Quick Summary is the most important part of every memory file. It must always reflect the file's current state.

**When to update the Quick Summary:**
- After every significant change to the file's content
- When the project's state has changed in a way that affects the summary
- When you notice the summary no longer matches reality

**Format reminder:**
```markdown
## Quick Summary
Architecture uses event-driven microservices with RabbitMQ for inter-service communication.
PostgreSQL for persistence, Redis for caching. Finalized 2025-01, cache layer added 2025-06.
```

The summary should answer: "What does this file tell me, and how current is it?"

## Staleness Detection

Memory files have a shelf life. A technical decision from 6 months ago may still be valid, or it may have been superseded by implementation changes that nobody documented.

**Staleness indicators:**
- File not modified in 30+ days (detected by `/review-memory`)
- Quick Summary references a project state that no longer exists
- The file describes an approach that was later abandoned
- Cross-references point to files that have been renamed or deleted

**When you encounter staleness:**

1. **Still accurate?** Update the timestamp to confirm it's been reviewed. No content change needed.
2. **Partially outdated?** Revise the outdated sections. Update the Quick Summary.
3. **Fully superseded?** Two options:
   - **Replace:** Rewrite the file with current knowledge. Keep the same filename and purpose.
   - **Archive:** If the knowledge category itself is no longer relevant, delete the file and remove it from the index. Don't keep dead files "just in case."

**Never** leave obviously stale content in place. A memory system with stale files trains Claude to distrust all memory content.

## Cross-Referencing

Memory files should reference each other when knowledge is related across categories.

**Good cross-references:**
```markdown
See `technical/issues-solutions.md` for the auth token refresh bug this decision addressed.
```

```markdown
The architecture decisions in `project/architecture.md` explain why this module uses WebSockets.
```

**Rules for cross-references:**
- Use relative paths from the memory root: `project/architecture.md`, not `../../memories/project/architecture.md`
- Reference the specific section when possible: `technical/issues-solutions.md#websocket-reconnection`
- Keep cross-references bidirectional when both files benefit
- Don't create circular reference chains — if A references B and B references A, make sure each reference adds value from that file's perspective

## Content Formatting

Memory files are reference documents, not narratives. Optimize for scanning and lookup.

**Prefer:**
- Tables for comparative information (alternatives considered, configuration values)
- Headers for distinct topics within a file
- Bullet points for lists of facts or decisions
- Code blocks for commands, configurations, or API responses

**Avoid:**
- Narrative prose that buries facts in paragraphs
- Long unstructured paragraphs
- Conversational tone ("So then we decided to...")
- Documenting the process of discovery rather than the discovery itself

**Example — good:**
```markdown
### WebSocket Reconnection (2025-03)
- **Problem:** Clients silently disconnect after 5 minutes of inactivity
- **Root cause:** Server-side keepalive timeout set to 300s, no client-side ping
- **Solution:** Added client-side ping every 60s, server keepalive extended to 600s
- **Related:** `project/architecture.md#real-time-layer`
```

**Example — bad:**
```markdown
### WebSocket Issue
We noticed that WebSocket connections were dropping. After some investigation,
we found that the server has a 5-minute timeout. We tried a few things but
eventually settled on adding a client-side ping every 60 seconds. We also
changed the server timeout to 10 minutes to be safe.
```

## Memory Eviction

Not all memory should be kept forever. Evict when:

- The knowledge was specific to a dependency version that has since been upgraded
- A temporary workaround was documented but the underlying issue has been properly fixed
- The project has pivoted and an entire category of memory is no longer relevant
- A file has been stale for 90+ days and nobody has referenced it

**Eviction process:**
1. Confirm the file is truly no longer useful (two-reader test)
2. Remove the file
3. Remove it from `index.md`
4. If the knowledge is partly relevant, extract the still-useful portions into another file before deleting
