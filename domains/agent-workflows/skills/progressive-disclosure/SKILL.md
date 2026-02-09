---
name: progressive-disclosure
description: >
  Design and maintain file-based progressive disclosure memory systems for Claude Code
  projects. Use when a project needs durable knowledge persistence across sessions —
  architecture decisions, technical learnings, domain expertise, or people context that
  outlasts any individual task. Triggers include requests for "project memory", "session
  persistence", "knowledge base", "memories directory", "progressive disclosure",
  "remember across sessions", or "capture learnings". Complements the autonomous-loop
  skill: loops handle intra-task state (progress.txt), memory systems handle institutional
  knowledge that accumulates over the lifetime of a project.
---

# Progressive Disclosure Memory System

Design and maintain structured, file-based memory systems that give Claude Code projects durable institutional knowledge. Unlike autonomous loop state files (which track task progress within a bounded goal), memory systems capture the open-ended knowledge a project accumulates over time — why an architecture was chosen, what technical approaches failed, how a domain's terminology maps to implementation, who prefers what.

## Core Mental Model

A memory system is a `memories/` directory with files organized by purpose, navigated through progressive disclosure. The key insight: **information should be layered so readers choose their depth.** Claude doesn't need to read every memory file at session start — it reads the index, identifies what's relevant, and dives only where needed.

```
memories/
├── index.md              ← Level 1: one-sentence per directory
├── project/              ← Level 2: category directories
│   ├── overview.md       ← Level 3: Quick Summary at top of each file
│   ├── architecture.md   ← Level 4: full detailed content below summary
│   └── roadmap.md        ← Level 5: CLI commands, deep references at bottom
├── technical/
│   ├── issues-solutions.md
│   └── environment.md
└── creative/
    ├── design-decisions.md
    └── user-preferences.md
```

### The Five Levels

**Level 1 — Index.** `memories/index.md` lists each directory with a one-sentence description. A reader should know which directory to enter without reading anything else. This is the entry point for every session.

**Level 2 — Directory.** Each subdirectory groups files by purpose. The directory name itself communicates what kind of knowledge lives inside: `project/` for meta-decisions, `technical/` for implementation learnings, `creative/` for domain-specific aesthetic or design decisions.

**Level 3 — Quick Summary.** Every memory file starts with a Quick Summary section — 1-2 sentences describing the file's contents and current state. Claude can read all Quick Summaries in a directory in seconds to decide which file deserves a full read. This is the scan-before-dive mechanism.

**Level 4 — Full Content.** The body of the memory file. Tables, narratives, decision records, analysis results. Organized for reference, not for storytelling. A reader who reaches this level wants specifics.

**Level 5 — Deep References.** The bottom of technical files may include CLI commands, links to external resources, or cross-references to other memory files. This is the "go deeper" escape hatch for when the file itself isn't enough.

### How Claude Uses This at Session Start

1. Read `memories/index.md` (seconds — just directory descriptions)
2. Based on the current task, identify which directories are relevant
3. Scan Quick Summaries in those directories (seconds per directory)
4. Read full content only for files that are directly relevant
5. Proceed with work, informed by durable project knowledge

This prevents context window flooding. A project with 20 memory files doesn't need all 20 loaded — progressive disclosure lets Claude load 2-3 relevant ones after a fast scan.

## Default Category Structure

Three categories cover most projects. Customize when a project's domain demands it, but start here.

### `project/`
Why the project exists and how it's structured. Decisions that affect the whole codebase.

| File | Contains |
|------|----------|
| `overview.md` | Project purpose, constraints, goals, key stakeholders |
| `architecture.md` | Technical decisions and their rationale — why X over Y |
| `roadmap.md` | Development phases, current progress, what's next |

### `technical/`
What was learned through implementation. The knowledge that prevents re-discovery of the same solutions and re-investigation of the same problems.

| File | Contains |
|------|----------|
| `issues-solutions.md` | Problems encountered and their fixes — the troubleshooting knowledge base |
| `environment.md` | Build setup, tool versions, platform-specific quirks, CI configuration |

### `creative/`
Domain-specific decisions that reflect taste, philosophy, or design intent. Not every project needs this — it matters most when the project has aesthetic, experiential, or domain-modeling dimensions.

| File | Contains |
|------|----------|
| `design-decisions.md` | Why the UX/UI/interaction model works the way it does |
| `user-preferences.md` | End-user or stakeholder preferences that inform decisions |

### When to Add Custom Categories

Add a new category when a project accumulates knowledge that doesn't fit the defaults:

- **`people/`** — When the project involves multiple people whose preferences, roles, or context matter across sessions. Each person gets their own file. Useful for tools with multiple users, client projects, or collaborative systems.
- **`domain/`** — When the project operates in a specialized domain (audio engineering, medical imaging, financial modeling) and domain-specific terminology, constraints, or best practices need to be captured.
- **`sessions/`** — When auto-generated session logs are desired for auditing. Use sparingly — session logs are chronological and tend toward noise. Purpose-organized files are almost always more useful.

**Do not** create a category for a single file. If only one file would live in the category, put it in the closest existing category instead.

## The Index File

`memories/index.md` is the navigation hub. Its structure is fixed:

```markdown
# Memory System Index

## Navigation Principle: Progressive Disclosure
Start with this index. Read Quick Summaries in relevant directories.
Dive into full content only when needed for the current task.

## Directories

### project/
Development context: why this project exists, architecture decisions, current progress.
- `overview.md` — Project purpose, constraints, and goals
- `architecture.md` — Technical decisions and their rationale
- `roadmap.md` — Development phases, current progress, next steps

### technical/
Implementation learnings: problems encountered, solutions found, environment setup.
- `issues-solutions.md` — Problems and their fixes
- `environment.md` — Build setup, tool versions, platform quirks

### creative/
Domain-specific decisions: design philosophy, user preferences, aesthetic choices.
- `design-decisions.md` — UX/UI/interaction design rationale
- `user-preferences.md` — Stakeholder preferences that inform decisions

## Update Guidelines
1. Keep Quick Summaries current — they're the first thing readers see
2. Add timestamps to significant updates
3. Cross-reference related files across directories
4. Remove stale information rather than letting it accumulate
```

Every file listed in the index includes a one-sentence description. The reader should know whether to open the file based solely on this sentence.

For complete guidance on writing effective index files, see `references/index-patterns.md`.

## Quick Summary Convention

Every memory file starts with this pattern:

```markdown
# File Title

## Quick Summary
[1-2 sentences: what this file contains and its current state]

## [Rest of the file's content sections]
...
```

Good Quick Summaries are **current and specific:**
- "Architecture uses event-driven microservices with RabbitMQ. Decision finalized 2025-01."
- "Three open issues: auth token refresh, WebSocket reconnection, and CSS grid fallback."
- "Phase 3 (API integration) complete. Phase 4 (testing) starts next session."

Bad Quick Summaries are **vague or stale:**
- "This file contains architecture information." (too vague)
- "Project overview." (restates the filename)
- Summary says "Phase 2 in progress" but the file body shows Phase 4 is done (stale)

## Memory vs Autonomous Loop State

These systems are complementary, not competing:

| Concern | Autonomous Loop State | Progressive Disclosure Memory |
|---------|----------------------|------------------------------|
| **Scope** | One bounded task | Entire project lifetime |
| **Files** | `feature_list.json`, `progress.txt` | `memories/` directory tree |
| **Persistence** | Until task completes, then archived | Indefinite — revised, never deleted without replacement |
| **Consumer** | The loop script + Claude session | Any Claude session working on the project |
| **Update trigger** | Every session (mandatory) | When meaningful work produces learnings (hook-enforced) |
| **Organization** | Flat (2-3 files) | Hierarchical (index → categories → files) |

A project can use both: the autonomous loop skill for running extended coding sessions, and the memory system for maintaining the institutional knowledge that informs all sessions — looped or interactive.

## Deterministic Capture with Stop Hooks

The memory system's enforcement mechanism is a Stop hook that blocks session exit when meaningful work wasn't captured in memory. The hook uses deterministic keyword scanning — not LLM judgment.

**How it works:**
1. When Claude tries to stop, the hook script reads the session transcript
2. It scans for meaningful work keywords: `implemented`, `fixed`, `created`, `refactored`, `discovered`, `learned`, `solution`, `decided`, `architected`, `debugged`, `optimized`, `migrated`, `integrated`
3. It checks whether any memory files were written or edited during the session
4. If meaningful work happened AND memory wasn't updated → the hook blocks exit with routing guidance

**Why deterministic?** Because the alternative — asking Claude "was this session important enough to persist?" — is subjective and inconsistent. Keyword scanning is predictable: the user always knows why the hook fired, and it never silently lets important work slip through.

See `hooks/memory-capture-stop.md` in this domain for the complete hook implementation.

## Further Reading

For specific deep-dive guidance, read the following reference files as needed:

- `references/memory-organization.md` — Deep patterns for by-purpose organization, anti-patterns to avoid, and when session logs help vs hurt
- `references/update-guidelines.md` — Rules for maintaining memory freshness, the two-reader test, and when to revise vs archive
- `references/index-patterns.md` — Writing effective index files, one-sentence descriptions, and template structures
