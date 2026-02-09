Audit the health of a progressive disclosure memory system and report findings.

If a path is provided as an argument, audit that directory. Otherwise, look for `memories/` in the current working directory. If no memory directory is found, report that and exit.

## Audit Process

Read all files in the memory directory and evaluate against the progressive disclosure standards.

### Check 1: Index Integrity

Read `memories/index.md` and compare against the actual directory contents.

- **MISSING_FROM_INDEX**: Files that exist on disk but aren't listed in the index
- **GHOST_ENTRY**: Files listed in the index that don't exist on disk
- **MISSING_INDEX**: No `index.md` found in the memory root

### Check 2: Quick Summaries

Read the first 10 lines of every memory file (except index.md files).

- **MISSING_SUMMARY**: File does not have a "Quick Summary" section in its first 10 lines
- **STALE_SUMMARY**: Quick Summary content appears to contradict later sections in the file (check for obvious version mismatches, e.g., summary says "Phase 2" but body discusses "Phase 5")

### Check 3: Staleness

Check modification timestamps on all memory files.

- **STALE_30**: File not modified in 30-60 days — review for freshness
- **STALE_90**: File not modified in 90+ days — likely needs revision or eviction

### Check 4: File Size

Count lines in each memory file.

- **OVERSIZED**: File exceeds 200 lines — consider splitting into focused sub-files
- **UNDERSIZED**: File has fewer than 5 lines of content (excluding headers) — may be a placeholder

### Check 5: Orphaned Files

Check for memory files (.md) not referenced from any index.md file in the memory directory.

- **ORPHANED**: File exists but no index references it — add to index or delete

### Check 6: Cross-References

Scan all memory files for references to other memory files (patterns like `category/filename.md`).

- **BROKEN_REFERENCE**: A cross-reference points to a file that doesn't exist
- **ONE_WAY_REFERENCE**: A references B but B doesn't reference A (informational, not always a problem)

### Check 7: Empty Categories

Check each subdirectory of the memory root.

- **EMPTY_CATEGORY**: Directory exists but contains no memory files — remove or populate

## Output Format

```
## Memory System Health Report

**Memory path:** memories/
**Total files:** <count>
**Total categories:** <count>

### Findings

#### CRITICAL
- [GHOST_ENTRY] index.md references `technical/api-design.md` but file does not exist
- [MISSING_INDEX] No index.md found

#### WARNING
- [STALE_90] `project/architecture.md` — last modified 95 days ago
- [OVERSIZED] `technical/issues-solutions.md` — 287 lines, consider splitting
- [ORPHANED] `technical/old-notes.md` — not referenced from any index

#### INFO
- [STALE_30] `creative/design-decisions.md` — last modified 42 days ago
- [MISSING_SUMMARY] `project/overview.md` — no Quick Summary section found
- [UNDERSIZED] `creative/user-preferences.md` — only 3 lines of content

### Summary
- Critical: <count>
- Warnings: <count>
- Info: <count>

### Recommended Actions
1. <most important action based on findings>
2. <second most important>
3. <third most important>
```

## Severity Levels

| Severity | Findings | Impact |
|----------|----------|--------|
| CRITICAL | GHOST_ENTRY, MISSING_INDEX, BROKEN_REFERENCE | Memory system is actively misleading — Claude will try to read nonexistent files |
| WARNING | STALE_90, OVERSIZED, ORPHANED, EMPTY_CATEGORY | Memory system is degrading — knowledge is being lost or becoming unfindable |
| INFO | STALE_30, MISSING_SUMMARY, UNDERSIZED, STALE_SUMMARY, ONE_WAY_REFERENCE | Memory system works but could be improved |

## Recommended Actions

Based on findings, suggest the 3 most impactful actions. Prioritize:
1. Fixing CRITICAL issues first (index integrity, broken references)
2. Addressing STALE_90 files (revise, update, or evict)
3. Adding missing Quick Summaries
4. Splitting oversized files
5. Resolving orphaned files

$ARGUMENTS
