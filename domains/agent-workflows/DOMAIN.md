# Agent Workflows Domain

## Scope

Patterns, skills, and tooling for orchestrating Claude Code as an autonomous or semi-autonomous agent. This domain covers the meta-layer — how to configure, harness, and control Claude Code sessions for extended operation, iterative development loops, and multi-session persistence.

### In Scope
- Autonomous agentic loop design (Ralph Wiggum methodology and variants)
- State persistence across context window boundaries
- Hook configuration for agent lifecycle control (Stop, PreToolUse, PostToolUse)
- Circuit breakers, stagnation detection, and recovery strategies
- Session handoff patterns (progress files, state files, git-based checkpointing)
- CLAUDE.md configuration patterns for autonomous operation
- MCP server configuration for agent workflows
- Cost and iteration budgeting for long-running sessions

### Out of Scope
- Domain-specific implementation (that's what UE5 C++, technical design, etc. handle)
- Claude Code's internal architecture or API internals
- Prompt engineering for conversational (non-agentic) use cases
- CI/CD pipeline design (except where Claude Code integrates with it)

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

## Conventions

### State Files Are Source of Truth
JSON state files (feature_list.json, checklist.md, spec_requirements.json) are the canonical record of what's done and what isn't. The agent may only modify the status fields after verification.

### One Task Per Session
Autonomous sessions work on exactly one item from the state file. This prevents partial completion of multiple items and makes rollback straightforward.

### Verify Before Marking Complete
No item is marked as passing/complete until tests actually pass. The Stop hook enforces this, but the CLAUDE.md instructions reinforce it as a protocol rule.

### Progress Notes Are Mandatory
Every session ends by updating progress.txt with: what was done, what's blocked, decisions made, and next steps. This is the anti-amnesia mechanism.

## Cross-Domain Connections

- **All domains**: Any domain's agents and commands can be deployed into a project that also uses an autonomous loop skill. The loop handles orchestration; domain content handles the actual work.
- **Templates**: Autonomous loop skills can be bundled into project templates. A template could include both the project scaffold and the loop infrastructure.
- **Technical Design**: Loop skills often implement specs — the technical-design domain's spec translator can produce the feature_list.json that an autonomous loop consumes.
