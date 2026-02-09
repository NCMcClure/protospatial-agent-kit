# Memory Organization Patterns

Deep reference on organizing project memory by purpose. Covers the fundamental trade-off between chronological and purpose-based organization, common patterns, and anti-patterns to avoid.

## By-Purpose vs By-Time

The most important organizational decision in a memory system: do files represent **what was learned** or **when it was learned**?

### By-Purpose (Recommended Default)

Files are named for the knowledge they contain. A file called `technical/audio-normalization.md` captures everything known about audio normalization — discoveries from session 1, corrections from session 5, the final working approach from session 12. All in one place, always current.

**Strengths:**
- Knowledge accumulates in one location, making it easy to find
- Files stay useful indefinitely because they represent understanding, not events
- Claude can load exactly the knowledge needed for the current task
- Naturally supports progressive disclosure (Quick Summary → details)

**When it works best:**
- Long-lived projects where knowledge compounds over time
- Projects with recurring topics (the same technical area keeps coming up)
- Any project where Claude needs to reference past decisions during current work

### By-Time (Use Sparingly)

Files are named for when events happened. A `sessions/` directory with files like `2025-02-04-14-30.md` records what happened in each session chronologically.

**Strengths:**
- Easy to create (just dump what happened)
- Provides an audit trail
- Useful for compliance or accountability scenarios

**When it fails:**
- Nobody reads them. Session logs accumulate and become noise.
- Finding "what do we know about X?" requires reading every log file and mentally aggregating
- Claude loads a session log, gets context about what happened on that day, and gets no help for today's problem
- They grow without bound — no natural consolidation mechanism

### The Hybrid Approach

Some projects benefit from both. Use purpose-organized files as the primary memory system, and optionally add a `sessions/` directory for audit trails. The stop hook should route knowledge to purpose files, not session logs. Session logs are generated as a side effect, not as the primary capture mechanism.

**Rule of thumb:** If a fact would be useful in a future session regardless of context, it belongs in a purpose file. If it only matters as a record of what happened, it can go in a session log (or be omitted entirely).

## Common Organization Patterns

### Pattern: The Three-Category Default

```
memories/
├── project/      ← decisions, architecture, roadmap
├── technical/    ← implementation learnings, issues, environment
└── creative/     ← domain-specific design, aesthetics, UX
```

Works for 80% of projects. Start here and add categories only when a clear need emerges.

### Pattern: People-Centric Memory

```
memories/
├── project/
├── technical/
└── people/
    ├── index.md       ← template for person files
    ├── alice.md       ← Alice's preferences, context, past interactions
    └── bob.md         ← Bob's context
```

Add `people/` when a project involves multiple stakeholders whose individual preferences or context matters across sessions. Each person gets their own file. Common in client-facing work, collaborative tools, or any project where "what does this person care about?" is a recurring question.

### Pattern: Domain-Heavy Memory

```
memories/
├── project/
├── technical/
├── domain/
│   ├── glossary.md           ← domain terminology mappings
│   ├── constraints.md        ← domain-specific rules and regulations
│   └── reference-data.md     ← key data points, benchmarks, standards
└── creative/
```

Add `domain/` when the project operates in a specialized field (medicine, finance, audio engineering, game design) and domain-specific knowledge needs its own namespace to avoid cluttering `technical/` with non-implementation concerns.

### Pattern: Multi-Module Memory

```
memories/
├── project/
├── technical/
│   ├── issues-solutions.md
│   ├── module-auth.md        ← module-specific learnings
│   ├── module-payments.md
│   └── module-notifications.md
└── creative/
```

For large codebases with distinct modules, create per-module technical memory files. Each file captures the implementation knowledge specific to that module — its quirks, its integration points, its failure modes.

## Anti-Patterns

### Anti-Pattern: Chronological Dumping

Creating a new file for every session or every day.

```
memories/
├── 2025-01-15.md
├── 2025-01-16.md
├── 2025-01-17.md
├── 2025-01-18.md
└── ... (50 more files)
```

**Why it fails:** Knowledge is scattered across files by accident of timing. To answer "what's our auth approach?" you'd need to grep 50 files. The signal-to-noise ratio drops with every new file.

**Fix:** Consolidate into purpose files. Extract the auth decisions from those 50 files into a single `technical/authentication.md`.

### Anti-Pattern: Flat File Dump

All memory files in a single directory with no categorization.

```
memories/
├── api-design.md
├── auth-tokens.md
├── bob-preferences.md
├── build-issues.md
├── css-grid-quirks.md
├── deployment.md
└── ... (20 more files)
```

**Why it fails:** No progressive disclosure. Claude has to scan every filename to find relevant content. With 20+ files, this wastes context window and time.

**Fix:** Introduce category directories. Group related files under `project/`, `technical/`, `creative/`, or `people/`. The index provides the first layer of navigation.

### Anti-Pattern: Memory Hoarding

Capturing everything, regardless of future utility.

**Symptoms:**
- Memory files that record ephemeral debugging steps that won't recur
- Files that document one-time setup procedures (belongs in README, not memory)
- Capturing "we tried X and it didn't work" without recording WHY it didn't work (the lesson)

**Fix:** Apply the two-reader test (see `update-guidelines.md`). Before writing to memory, ask: will this be useful to a future Claude session OR to the human reading it? If neither, don't capture it.

### Anti-Pattern: Orphaned Memories

Files that exist but are never referenced from any index and never read.

**Why it happens:** A file was created, the index wasn't updated, and the file becomes invisible. Claude doesn't know to look for it because nothing points to it.

**Fix:** The `/review-memory` command detects orphaned files. Keep the index current whenever files are added or removed.

## Memory Convergence

When two or more memory files start containing overlapping information, consolidate.

**Signals that convergence is needed:**
- You find yourself updating the same fact in two files
- Cross-references between files have become circular
- A new reader wouldn't know which file to consult for topic X

**How to converge:**
1. Identify the overlapping content
2. Choose the canonical file (the one whose purpose best fits the knowledge)
3. Move the content to the canonical file
4. Replace the content in the other file(s) with a cross-reference
5. Update the index to reflect the change

Convergence keeps the memory system honest. A 5-file memory system where each file has a clear, distinct purpose is more valuable than a 15-file system with overlapping, redundant content.
