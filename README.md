# Protospatial Agent Kit

A personal agent toolkit for technical designers spanning a variety of different machine learning, software engineering, design, and realtime 3D use-cases. Clone it anywhere, open Claude Code, tell it what you need — it extracts existing tooling to target projects and creates new Claude Code artifacts with consistent standards.

## What's Inside

### Domains

| Domain | Contents | Description |
|--------|----------|-------------|
| [UE5 C++](domains/ue5-cpp/) | 2 agents, 2 commands, 2 prompts | UE5 plugin/systems C++ — code review, class architecture, conventions reference |
| [Technical Design](domains/technical-design/) | 2 agents, 2 commands, 2 prompts | Design-engineering bridge — spec translation, prototype planning, vocabulary mapping |
| [Agent Workflows](domains/agent-workflows/) | 2 skills, 1 agent, 2 commands, 1 prompt, 2 hooks | Autonomous agentic loops, progressive disclosure memory systems, session persistence, hooks, circuit breakers |

### Templates

| Template | Description |
|----------|-------------|
| [ue5-plugin](templates/ue5-plugin/) | Bootstrap a new UE5 C++ plugin project with CLAUDE.md, commands, and gitignore |

### References

| Reference | Description |
|-----------|-------------|
| [Claude Code Artifacts](references/claude-code-artifacts.md) | Format specs for every Claude Code artifact type — commands, agents, skills, hooks, settings, templates |

## Usage

```
# Clone to any machine
git clone <repo-url> protospatial-agent-kit

# Open Claude Code in the kit
cd protospatial-agent-kit
claude

# Extract tooling to a project:
# "Set up the ue5-plugin template at F:\Projects\MyNewPlugin"
# "Copy the code reviewer agent to F:\Projects\NodeToCode\.claude\agents\"
# "I need the design-to-spec command in my current project"

# Create new kit content:
# "Create a new agent for reviewing Slate widget code"
# "Add a command that audits a project's CLAUDE.md"
# "I need a new domain for XR spatial computing"
```

### Kit Commands

| Command | Purpose |
|---------|---------|
| `/extract` | Deploy kit content (templates, agents, commands, prompts) to a target project |
| `/create` | Create new kit content following the established format standards |

## Structure

```
.claude/commands/  Kit management commands (/extract, /create)
domains/           Per-domain agents, commands, and prompts
  <domain>/
    DOMAIN.md      Scope, conventions, key concepts
    agents/        Specialized agent definitions
    commands/      Slash command definitions
    prompts/       Reference knowledge bases
templates/         Exportable project scaffolds
  <template>/
    TEMPLATE.md    Description and usage
    *.template     Files with {{VARIABLE}} substitution
references/        Cross-cutting reference documentation
```

## Growing the Kit

This kit grows organically. When you find a pattern, agent, command, or prompt that you keep reaching for across projects — add it here.

- **Use `/create`** for guided creation of any artifact type with the right format
- **Use `/extract`** to deploy it wherever you need it next
- **Check `references/claude-code-artifacts.md`** for format specs when building artifacts manually

Every artifact has a defined format. Commands are verbs. Agents are specialists. Prompts are reference. Skills are expertise. No placeholders — everything has real content.
