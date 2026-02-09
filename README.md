# Protospatial Agent Kit

A personal agent toolkit for a senior XR/ML technical designer. Clone it anywhere, open Claude Code, tell it what you need and where — it extracts and installs the relevant tooling.

## What's Inside

### Domains

| Domain | Contents | Description |
|--------|----------|-------------|
| [UE5 C++](domains/ue5-cpp/) | 2 agents, 2 commands, 2 prompts | UE5 plugin/systems C++ — code review, class architecture, conventions reference |
| [Technical Design](domains/technical-design/) | 2 agents, 2 commands, 2 prompts | Design-engineering bridge — spec translation, prototype planning, vocabulary mapping |

### Templates

| Template | Description |
|----------|-------------|
| [ue5-plugin](templates/ue5-plugin/) | Bootstrap a new UE5 C++ plugin project with CLAUDE.md, commands, and gitignore |

## Usage

```
# Clone to any machine
git clone <repo-url> protospatial-agent-kit

# Open Claude Code in the kit
cd protospatial-agent-kit
claude

# Then just tell it what you need:
# "Set up the ue5-plugin template at F:\Projects\MyNewPlugin"
# "Copy the code reviewer agent to F:\Projects\NodeToCode\.claude\agents\"
# "I need the design-to-spec command in my current project"
```

Or use the `/extract` command for guided extraction.

## Structure

```
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
```

## Growing the Kit

This kit grows organically. When you find a pattern, agent, command, or prompt that you keep reaching for across projects — add it here. Use `/extract` to deploy it wherever you need it next.
