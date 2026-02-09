# Index File Patterns

How to write effective `memories/index.md` files that serve as navigation hubs for progressive disclosure memory systems.

## Purpose of the Index

The index is the entry point to the entire memory system. Its job is to answer one question: **"Where should I look?"** A reader (Claude or human) should be able to scan the index and know which directory and which file to open — without reading anything else first.

## Core Structure

Every index follows this template:

```markdown
# Memory System Index

## Navigation Principle: Progressive Disclosure
Start with this index. Read Quick Summaries in relevant directories.
Dive into full content only when needed for the current task.

## Directories

### <category-name>/
[One-sentence description of what knowledge lives here.]
- `<filename>.md` — [One-sentence description of this file's contents]
- `<filename>.md` — [One-sentence description]

### <category-name>/
[One-sentence description.]
- `<filename>.md` — [One-sentence description]

## Update Guidelines
1. Keep Quick Summaries current — they're the first thing readers see
2. Add timestamps to significant updates
3. Cross-reference related files across directories
4. Remove stale information rather than letting it accumulate
```

## Writing One-Sentence Descriptions

The directory and file descriptions are the most critical text in the index. They must be:

**Specific enough to be useful:**
- "Technical decisions about infrastructure, data layer, and service architecture" (directory)
- "PostgreSQL schema evolution and migration approach" (file)
- "Known issues with the WebSocket reconnection logic and their workarounds" (file)

**Not so generic they say nothing:**
- "Technical stuff" (useless)
- "Various notes" (useless)
- "Important decisions" (useless — all decisions in memory should be important)

**Current:**
- "Phase 3 complete; Phase 4 (testing) in progress" (tells you the state)
- Not: "Development phases and progress" (timeless but uninformative)

## Index Maintenance Rules

### Add to the Index When

- A new memory file is created → add it with a one-sentence description
- A new directory is created → add the directory with its description
- A file's scope has changed significantly → update its description

### Remove from the Index When

- A memory file is deleted or archived → remove the entry
- A directory is empty → remove the directory section
- A file has been renamed → update the reference

### Never

- List files that don't exist (creates confusion when Claude tries to read them)
- Use placeholder descriptions ("TBD", "TODO", "will fill in later")
- Let the index grow stale while files are actively updated

## Scaling the Index

For small projects (5-10 files), the default template works as-is.

For larger projects (15+ files), add a **Quick Status** section at the top:

```markdown
## Quick Status
- **Active focus:** API migration (Phase 3)
- **Recent updates:** technical/api-migration.md (2025-03-15), project/roadmap.md (2025-03-14)
- **Needs attention:** creative/design-decisions.md (stale 45d)
```

This gives Claude a 3-second orientation before even scanning directories.

## Multiple Index Files

Each directory can optionally have its own `index.md` for intra-directory navigation. This is useful when a directory has 5+ files:

```
memories/
├── index.md                  ← top-level navigation
├── technical/
│   ├── index.md              ← navigates within technical/
│   ├── issues-solutions.md
│   ├── api-migration.md
│   ├── database-schema.md
│   ├── performance-tuning.md
│   └── deployment-notes.md
```

The directory-level `index.md` follows the same pattern: one-sentence per file, organized for scan-before-dive.

**Don't** create directory-level index files for directories with fewer than 4 files. The top-level index already lists those files — a redundant index adds maintenance burden without navigation value.

## Template for a New Project

When bootstrapping a memory system (via `/init-memory`), start with this minimal index:

```markdown
# Memory System Index

## Navigation Principle: Progressive Disclosure
Start with this index. Read Quick Summaries in relevant directories.
Dive into full content only when needed for the current task.

## Directories

### project/
Why this project exists, how it's structured, and where it's headed.
- `overview.md` — Project purpose, constraints, and goals
- `architecture.md` — Technical decisions and their rationale
- `roadmap.md` — Development phases, current progress, next steps

### technical/
Implementation learnings accumulated through building and debugging.
- `issues-solutions.md` — Problems encountered and their fixes
- `environment.md` — Build setup, tool versions, platform-specific quirks

### creative/
Domain-specific design decisions and stakeholder preferences.
- `design-decisions.md` — UX/UI/interaction design rationale
- `user-preferences.md` — Stakeholder preferences that inform decisions

## Update Guidelines
1. Keep Quick Summaries current — they're the first thing readers see
2. Add timestamps to significant updates
3. Cross-reference related files across directories
4. Remove stale information rather than letting it accumulate
```

Customize the directory structure and file list during initialization based on the project's needs. The template provides sensible defaults — not every project needs `creative/`, and some projects need `domain/` or `people/` instead.
