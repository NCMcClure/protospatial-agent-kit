# Claude Code Artifact Reference

Comprehensive reference for every artifact type that Claude Code recognizes. Use this when creating new agents, commands, skills, hooks, or other Claude Code configuration for this kit or any target project.

## Commands

**Location**: `.claude/commands/<command-name>.md`
**Invocation**: `/<command-name>` in Claude Code
**Frontmatter**: None

Commands are imperative instructions that Claude executes when the user invokes them via slash command. They produce output — they are verbs, not conversations.

### Format

```markdown
Brief description of what this command does.

[Detailed procedural instructions for Claude to follow]

[Output format specification]

$ARGUMENTS
```

### Rules

- **No frontmatter.** Commands are plain markdown. The file name becomes the slash command name.
- **File name = command name.** `build-check.md` becomes `/build-check`.
- **Kebab-case** file names only.
- **`$ARGUMENTS`** at the end captures anything the user types after the command name. Include it if the command accepts input.
- **Imperative mood.** Write as direct instructions to Claude: "Read the file", "Analyze the output", "Ask the user for...".
- **Structured output.** Specify what the command's output should look like. Commands that produce unpredictable output are hard to use.
- **Self-contained.** A command should work without requiring the user to explain what it does. The instructions ARE the explanation.

### Example

```markdown
Review the UE5 C++ class specified by the user.

If a file path is provided, read that file. If both .h and .cpp exist, review both.

Apply the review checklist:
1. Reflection system correctness
2. Memory & lifetime safety
3. Naming conventions
4. Module structure

Output a structured review with CRITICAL / WARNING / SUGGESTION / GOOD items.

$ARGUMENTS
```

---

## Agents

**Location**: `.claude/agents/<agent-name>.md`
**Invocation**: Used via Claude Code's agent mode or referenced by commands
**Frontmatter**: Required (YAML)

Agents are specialist definitions with narrow scope. They define who Claude should be when performing a specific type of work.

### Format

```markdown
---
name: <kebab-case-name>
description: <one-line description of the agent's role>
---

# Agent Display Name

You are a [specialist role description]. [Context for when/how this agent operates.]

## [Responsibilities / Checklist / Process]

[Detailed instructions organized by section]

## Output Format

[Exact format the agent should produce]

## Quality Standards

[What "good" looks like for this agent's output]
```

### Rules

- **Frontmatter is required.** Use `name` (kebab-case value) and `description`.
- **Narrow scope.** An agent that "helps with UE5" is useless. An agent that "reviews UE5 C++ for reflection macro correctness" is useful.
- **Structured output.** Always define what the agent produces. Reviews have severity levels. Designs have section templates. Analyses have structured findings.
- **Quality criteria.** Define what good output looks like so the agent can self-evaluate.
- **Role framing.** Start with "You are a..." to establish the agent's persona and expertise boundary.

### Example

```markdown
---
name: spec-translator
description: Translates between design language and engineering specifications bidirectionally
---

# Design-Engineering Spec Translator

You translate between design intent and technical specifications in both directions.

## Direction 1: Design → Technical Spec

### Process
1. Extract the design intent
2. Map subjective terms to concrete values
3. Identify implicit requirements
4. Produce the spec

## Output Format

### Design Intent
[2-3 sentences in the designer's language]

### Behavior
[Concrete terms with states and transitions]

### Open Questions
[Specific questions needing answers before implementation]
```

---

## Skills

**Location**: `.claude/skills/<skill-name>/SKILL.md` (plus optional supporting files in the same directory)
**Invocation**: Available as context/reference when working in the project
**Frontmatter**: Required (YAML)

Skills are knowledge bundles — a primary SKILL.md plus supporting reference files. Unlike commands (which are actions) and agents (which are roles), skills are knowledge that enhances Claude's capabilities in a specific area.

### Format

```markdown
---
name: <skill-name>
description: >
  Multi-line description of what knowledge
  or capability this skill provides
---

# Skill Display Name

[Core knowledge, frameworks, procedures, or reference material]

## [Organized sections of domain knowledge]

[Content that makes Claude better at this specific thing]
```

### Directory Structure

```
.claude/skills/
  my-skill/
    SKILL.md              # Primary skill definition (required)
    supporting-doc.md     # Additional reference material (optional)
    another-reference.md  # More supporting content (optional)
```

### Rules

- **Frontmatter uses `name`** and `description`.
- **Directory per skill.** Skills live in subdirectories, not as flat files.
- **SKILL.md is the entry point.** Claude reads this first. It can reference other files in the same directory.
- **Knowledge, not instructions.** Skills provide expertise that makes Claude better at a class of work. They're not step-by-step procedures (that's what commands are for).
- **Supporting files** should be referenced from SKILL.md so Claude knows they exist.

### Example

```markdown
---
name: atomic-design
description: >
  Brad Frost's Atomic Design methodology for
  component classification and design systems
---

# Atomic Design

A methodology for creating design systems with five tiers...

## Classification Framework

See `classification-guide.md` for the full decision tree.

## Design Tokens

See `design-tokens.md` for token naming conventions.
```

---

## Hooks

**Location**: `.claude/settings.json` (project-level, committed) or `.claude/settings.local.json` (personal, gitignored)
**Invocation**: Automatic — triggered by Claude Code events
**Format**: JSON within the settings file

Hooks are shell commands that execute automatically in response to Claude Code lifecycle events. They run before or after tool use, on notifications, and at other defined points.

### Format (within settings JSON)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "ToolName",
        "hooks": [
          {
            "type": "command",
            "command": "shell command to run"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Bash tool was used'"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Task complete'"
          }
        ]
      }
    ]
  }
}
```

### Event Types

| Event | When It Fires | Use Cases |
|-------|---------------|-----------|
| `PreToolUse` | Before a tool executes | Validation, logging, guards |
| `PostToolUse` | After a tool executes | Logging, formatting, post-processing |
| `Notification` | When Claude sends a notification | Desktop alerts, sound cues |
| `Stop` | When Claude stops generating | Cleanup, final validation |

### Rules

- **Matcher** filters which tool triggers the hook. Empty string matches everything.
- **Commands** are shell commands executed in the project root.
- **Hook output** is fed back to Claude as context. Use this for validation feedback.
- **Keep hooks fast.** They block Claude's workflow. Long-running hooks degrade the experience.
- **Project-level hooks** (`.claude/settings.json`) are committed and shared. **Personal hooks** (`.claude/settings.local.json`) are gitignored.

---

## Settings

**Location**: `.claude/settings.json` (shared/committed) or `.claude/settings.local.json` (personal/gitignored)
**Format**: JSON

### Structure

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(powershell*script.ps1*)",
      "Read(**)"
    ],
    "deny": [
      "Bash(rm -rf:*)"
    ]
  },
  "hooks": { },
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": [],
  "disabledMcpjsonServers": ["server-name"],
  "enabledPlugins": {
    "plugin-id@namespace": true
  }
}
```

### Permission Patterns

```
ToolName(pattern)
```

- `Bash(git*:*)` — any git command
- `Bash(powershell*scripts/bootstrap.ps1*)` — specific script
- `Read(**)` — read any file
- `mcp__server__tool-name` — specific MCP tool

### Which Settings File?

| Use Case | File | Committed? |
|----------|------|-----------|
| Shared project config (hooks, shared permissions) | `.claude/settings.json` | Yes |
| Personal preferences (permissions, plugins, MCP) | `.claude/settings.local.json` | No (gitignored) |

---

## CLAUDE.md

**Location**: Project root (and optionally in subdirectories for scoped context)
**Format**: Markdown (no frontmatter required)

The project-level system prompt. Claude reads this first when opening a project. It establishes identity, navigation, conventions, and quality standards.

### Effective Patterns

- **Identity first.** What is this project? What role should Claude play?
- **Navigation table.** Where is everything? Point to directories, key files, domains.
- **Conventions.** Naming, formatting, coding standards — concrete rules, not vague guidance.
- **Quality standards.** What does "good" look like? What's unacceptable?
- **Workflow guidance.** How to perform common tasks in this specific project.

### Nesting

CLAUDE.md in subdirectories provides scoped context for that area. Claude reads the root CLAUDE.md plus any CLAUDE.md in the directory it's working in. Subdirectory CLAUDE.md files supplement, they don't replace the root.

The `@AGENTS.md` include pattern (used in NodeToCode and ProtoUI) delegates detailed context to an AGENTS.md file:

```markdown
# ProjectName

@AGENTS.md
```

---

## Templates (Kit-Specific)

**Location**: `templates/<template-name>/`
**Purpose**: Exportable project scaffolds with variable substitution

### Structure

```
templates/<name>/
  TEMPLATE.md            # Documentation (not deployed)
  CLAUDE.md.template     # Deployed as CLAUDE.md with variable substitution
  .gitignore.template    # Deployed as .gitignore with variable substitution
  .claude/
    commands/
      some-command.md    # Deployed as-is (no substitution needed)
```

### Rules

- **`.template` extension** = file gets renamed (extension removed) and `{{VARIABLE}}` placeholders are substituted during extraction.
- **No `.template` extension** = file is copied as-is to the target.
- **`TEMPLATE.md`** documents the template (variables, usage, what's included). It is NOT deployed to the target.
- **Variables** use `{{VARIABLE_NAME}}` syntax (double curly braces, UPPER_SNAKE_CASE).

---

## Domain Content (Kit-Specific)

**Location**: `domains/<domain-name>/`
**Purpose**: Per-domain agents, commands, and prompts organized by specialty

### Structure

```
domains/<name>/
  DOMAIN.md              # Scope, conventions, key concepts (required)
  agents/
    agent-name.md        # Agent definitions (standard agent format)
  commands/
    command-name.md      # Command definitions (standard command format)
  prompts/
    reference-name.md    # Knowledge base reference docs
```

### DOMAIN.md Sections

1. **Scope** — What belongs in this domain (and what explicitly does not)
2. **Key Concepts** — Core ideas and terminology
3. **Conventions** — Domain-specific rules and patterns
4. **Cross-Domain Connections** — Where this domain overlaps with others

### Prompts

Prompts are reference knowledge bases, not instructions. They contain dense factual content that agents and commands draw from. They don't have frontmatter — they're pure markdown reference documents.
