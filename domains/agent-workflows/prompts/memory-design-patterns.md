# Memory Design Patterns

Reference knowledge base for designing and evaluating file-based project memory systems. This document covers patterns that work, anti-patterns to avoid, and the principles that distinguish useful memory from noise.

## The Memory Spectrum

File-based memory systems sit in a sweet spot between two extremes:

| Approach | Structure | Signal | Maintenance |
|----------|-----------|--------|-------------|
| No memory (ad hoc) | None | Zero — everything rediscovered every session | None |
| Unstructured notes | Flat files, no convention | Low — knowledge exists but is hard to find | Minimal but futile |
| **Structured markdown** | **Directories, index, Quick Summaries** | **High — knowledge findable and scannable** | **Moderate — index + summary upkeep** |
| Over-structured database | Schema, relations, queries | High but brittle — schema changes break things | Heavy — migration overhead |

Structured markdown wins for agent-project collaboration because:
- Claude reads markdown natively — no query language, no ORM, no schema
- Humans read markdown natively — no tools needed to inspect or edit memory
- Git tracks changes — memory has version history for free
- Progressive disclosure controls context window usage — no "load everything" problem
- Low ceremony — creating or updating a file is a single Write/Edit operation

## Organizational Patterns

### Pattern: Single Source of Truth

Every piece of knowledge should live in exactly one memory file. When the same fact appears in multiple files, updates become inconsistent and trust degrades.

**How to implement:**
- Before writing new knowledge, check if it fits in an existing file
- When knowledge spans categories, choose one canonical location and cross-reference from others
- If two files start overlapping, consolidate (see Convergence pattern below)

### Pattern: Knowledge Convergence

As a project matures, memory files may start containing overlapping information. This is a signal to consolidate.

**Triggers:**
- Updating the same fact in two or more files
- Cross-references between files become circular
- A reader wouldn't know which file to consult for topic X

**Resolution:**
1. Identify the canonical file (the one whose purpose best fits the knowledge)
2. Migrate overlapping content to the canonical file
3. Replace removed content with a one-line cross-reference
4. Update the index

**Goal:** Each file has a clear, distinct purpose. A 5-file system with no overlap beats a 15-file system with redundancy.

### Pattern: Memory Eviction

Not all knowledge should persist indefinitely. Eviction removes knowledge that no longer passes the two-reader test.

**Eviction candidates:**
- Workarounds for bugs in dependency versions that have been upgraded
- Temporary architectural compromises that have been properly resolved
- Domain knowledge for features that were removed or never shipped
- Files stale for 90+ days that nobody has referenced

**Eviction process:**
1. Confirm the knowledge is truly obsolete (check with the human if uncertain)
2. Extract any still-relevant fragments into other files
3. Delete the file
4. Remove from index

**Do not** archive for posterity. Git history preserves the old content if it's ever needed. The living memory system should contain only living knowledge.

### Pattern: Layered Reading Depth

Structure every file so readers can stop at any depth and have gotten useful information:

```
Level 1: File name in index → "issues-solutions.md — Problems and their fixes"
Level 2: Quick Summary → "Three open issues: auth refresh, WebSocket, CSS grid"
Level 3: Section headers → "### WebSocket Reconnection (2025-03)"
Level 4: Full content → Detailed problem/cause/solution
Level 5: References → Links to related files, CLI commands, external docs
```

This is progressive disclosure at the file level. A reader who only needs "do we have WebSocket issues?" gets their answer at Level 3. A reader who needs the fix gets it at Level 4.

### Pattern: Starter Files

When initializing memory, create files with structure but not placeholder content. Each file should have:

```markdown
# Technical Issues and Solutions

## Quick Summary
No issues recorded yet. This file will capture problems encountered during
implementation and their solutions, organized by component.

## Format
Each entry follows this structure:
- **Problem:** What went wrong or was unexpected
- **Root Cause:** Why it happened
- **Solution:** What fixed it
- **Related:** Cross-references to other memory files
```

This is NOT placeholder content — it's a format definition that guides future entries. The file is immediately useful as a template for the first real entry.

## Anti-Patterns

### Anti-Pattern: Memory Hoarding

Capturing every fact, decision, and observation regardless of future value.

**Symptoms:**
- Memory files with 50+ entries, most of which are trivial
- "Ran npm install" as a memory entry
- Debugging steps recorded in full detail (including wrong turns)
- Facts that are obvious from the code itself ("the API uses REST")

**Cause:** Treating memory as a log rather than a knowledge base. Logs record events; knowledge bases record understanding.

**Fix:** Apply the two-reader test before every memory write. Will a future Claude session need this? Will the human reference it? If neither, don't capture it.

### Anti-Pattern: Orphaned Memories

Files that exist in the memory directory but aren't listed in any index.

**Why it happens:** Files are created, the index isn't updated, and the file becomes invisible. Claude doesn't know to look for `technical/special-case.md` because nothing mentions it.

**Impact:** The knowledge exists but is never used. Worse, it may grow stale without anyone noticing.

**Fix:** Always update the index when creating or deleting memory files. Use `/review-memory` to detect orphans. The index is the contract — if a file isn't in the index, it doesn't exist as far as the memory system is concerned.

### Anti-Pattern: Context Window Flooding

Loading all memory files at session start "just in case."

**Why it fails:** Memory systems exist precisely to avoid this. A project with 20 memory files at 100 lines each puts 2,000 lines into context before any work begins. Most of it will be irrelevant to the current task.

**Fix:** Progressive disclosure. Read the index (20 lines). Identify relevant directories. Scan Quick Summaries (5 lines each). Load only the 1-3 files that matter for the current task. This is what the five-level system is designed for.

### Anti-Pattern: Documentation Misplacement

Putting content in memory that belongs elsewhere.

| Content Type | Belongs In | Not In |
|-------------|-----------|--------|
| How to build the project | README.md | memories/ |
| API endpoint documentation | Code comments or docs/ | memories/ |
| Commit message conventions | CLAUDE.md or CONTRIBUTING.md | memories/ |
| Why we chose PostgreSQL | memories/project/architecture.md | README.md |
| What we learned debugging auth | memories/technical/issues-solutions.md | Code comments |

**Rule of thumb:** Memory stores *why* and *what was learned*. Documentation stores *how* and *what exists*. If the content would go in a README in a non-memory-enabled project, it still goes in the README.

## The Two-Reader Test

The single most important quality gate for memory content.

**Before writing to memory, ask:**

1. **Will a future Claude session benefit from knowing this?**
   - Future sessions start with zero context. Does this knowledge help them orient faster, avoid past mistakes, or build on past decisions?

2. **Will the human benefit from this being recorded?**
   - When the human returns after a week away, will this help them remember why things are the way they are?

**If yes to either → capture it.**
**If no to both → skip it.**

This test prevents both hoarding (capturing everything) and under-capture (forgetting important things). It's the quality filter that keeps memory systems useful over time.

## Memory System Health Indicators

### Healthy System
- Index is current and matches the actual file structure
- Quick Summaries reflect current file state
- Files are organized by purpose, not chronology
- Each file has a distinct scope with minimal overlap
- Stale files are revised or evicted within 30 days
- Cross-references are bidirectional and valid

### Unhealthy System
- Index lists files that don't exist (or misses files that do)
- Quick Summaries contradict the file body
- Multiple files cover the same topic with conflicting information
- Session log files accumulate without consolidation
- Files haven't been updated in 90+ days
- No cross-references — files exist in isolation
