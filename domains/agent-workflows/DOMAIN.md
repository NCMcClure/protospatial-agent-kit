# Agent Workflows Domain

## Scope

Patterns, skills, and tooling for orchestrating Claude Code as an autonomous or semi-autonomous agent. This domain covers the meta-layer — how to configure, harness, and control Claude Code sessions for extended operation, iterative development loops, multi-session persistence, and durable project memory.

### In Scope
- Autonomous agentic loop design (Ralph Wiggum methodology and variants)
- State persistence across context window boundaries
- Hook configuration for agent lifecycle control (Stop, PreToolUse, PostToolUse)
- Circuit breakers, stagnation detection, and recovery strategies
- Session handoff patterns (progress files, state files, git-based checkpointing)
- CLAUDE.md configuration patterns for autonomous operation
- MCP server configuration for agent workflows
- Cost and iteration budgeting for long-running sessions
- File-based progressive disclosure memory systems
- Deterministic hook-based memory capture enforcement
- Memory lifecycle: initialization, capture, maintenance, eviction
- Index-based navigation patterns for hierarchical project memory

### Out of Scope
- Domain-specific implementation (that's what UE5 C++, technical design, etc. handle)
- Claude Code's internal architecture or API internals
- Prompt engineering for conversational (non-agentic) use cases
- CI/CD pipeline design (except where Claude Code integrates with it)
- Database-backed or API-driven memory systems (this domain covers file-based markdown memory only)
- Conversation history or chat log retention as a memory strategy

## Key Concepts

### Externalized Memory
The core insight behind autonomous loops: agent state lives on the filesystem, not in the context window. JSON state files, progress notes, and git history become the agent's persistent memory. When a context window fills and a fresh session starts, it reconstructs state by reading files — not by remembering.

### The Ralph Wiggum Loop
A bash `while` loop that continuously invokes `claude --print` with the same prompt. Each iteration reads state files, does one unit of work, updates state, and commits. Named for the "I'm in danger" meme — the agent doesn't know its context is about to reset, but it doesn't need to because everything important is already on disk.

### Stop Hook Validation
The critical safety mechanism. A Stop hook script runs when Claude tries to finish a session. It checks: did tests pass? Was the state file updated? Are there uncommitted changes? If validation fails, the hook blocks exit and forces Claude to fix the issue before continuing.

### Circuit Breaker
Detects when an autonomous loop has gone unproductive — no file changes for N iterations, same error repeating, or session duration exceeded. Triggers graceful shutdown rather than burning tokens on a stuck task.

### Session Handoff
The practice of writing detailed notes at the end of each session so the next session (which has zero memory of the previous one) can pick up exactly where work left off. The `progress.txt` file is the handoff artifact.

### Progressive Disclosure Memory
Knowledge organized in layers of increasing detail for durable project memory. Level 1 is a one-line directory description in an index. Level 5 is deep technical content with CLI references. A reader can stop at any level and have gotten useful orientation without loading everything into context. This is the organizational model for the `memories/` directory pattern.

### Memory by Purpose
Memory categories reflect WHY information matters (technical learnings, design decisions, domain expertise) rather than WHEN it was captured. A session log tells you what happened on Tuesday — a purpose-organized file tells you everything known about the audio normalization approach, regardless of when each piece was learned. Purpose-organized files stay useful indefinitely; chronological dumps become noise.

### Quick Summary
The convention that every memory file begins with a 1-2 sentence summary of what the file contains and its current state. This enables rapid context loading: Claude reads all Quick Summaries in a directory to decide which file to read in full, without loading everything into the context window.

### Deterministic Capture
Stop hooks enforce memory updates using keyword-based transcript scanning — not LLM judgment calls. The hook scans for meaningful work indicators (implemented, fixed, discovered, etc.) and blocks session exit if work was done but memory was not updated. Deterministic means predictable: the user knows exactly when the hook fires and why. No false positives from subjective "importance" assessment.

## Conventions

### State Files Are Source of Truth
JSON state files (feature_list.json, checklist.md, spec_requirements.json) are the canonical record of what's done and what isn't. The agent may only modify the status fields after verification.

### One Task Per Session
Autonomous sessions work on exactly one item from the state file. This prevents partial completion of multiple items and makes rollback straightforward.

### Verify Before Marking Complete
No item is marked as passing/complete until tests actually pass. The Stop hook enforces this, but the CLAUDE.md instructions reinforce it as a protocol rule.

### Progress Notes Are Mandatory
Every session ends by updating progress.txt with: what was done, what's blocked, decisions made, and next steps. This is the anti-amnesia mechanism.

### Memory Files Start with Quick Summary
Every file in a `memories/` directory must begin with a Quick Summary section — 1-2 sentences describing the file's purpose and current state. This is the progressive disclosure contract: readers can scan summaries to find what they need without reading full documents.

### Memory is Organized by Purpose
Memory directories use categories that reflect the type of knowledge (project decisions, technical learnings, domain expertise) rather than when the knowledge was captured. The default categories are `project/`, `technical/`, and `creative/`, but projects customize based on their domain.

### Memory Updates Use Timestamps
Significant updates to memory files include a date stamp so readers can assess freshness. Stale information is revised or archived, never silently left to rot.

## Cross-Domain Connections

- **All domains**: Any domain's agents and commands can be deployed into a project that also uses an autonomous loop skill or a memory system. Loops handle orchestration; memory handles institutional knowledge; domain content handles the actual work.
- **All domains (memory)**: Any domain's agents and commands benefit from a project memory system. The UE5 code reviewer can reference `memories/technical/` for known issues. The spec translator can reference `memories/project/` for architecture decisions. Memory provides context; domain agents provide expertise.
- **Templates**: Autonomous loop skills and memory systems can be bundled into project templates. A template could include both the project scaffold and the persistence infrastructure.
- **Technical Design**: Loop skills often implement specs — the technical-design domain's spec translator can produce the feature_list.json that an autonomous loop consumes.
