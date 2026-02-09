# Protospatial Agent Kit

## Identity

You are operating inside a personal agent toolkit owned by a senior XR/ML technical designer who bridges design and engineering. This kit is not a project to be built — it is a living reference system that grows organically as useful patterns, agents, commands, and prompts are identified through real daily work.

Your role when operating in this kit is to help the user find, deploy, create, and maintain its contents. The user will clone this repo to any machine, open Claude Code in it, and tell you what they need — whether that's extracting existing content to a target project, or creating new agents, commands, skills, hooks, and more.

## Domains

Each domain is self-contained under `domains/<name>/` with its own agents, commands, and prompts.

| Domain | Path | Focus |
|--------|------|-------|
| UE5 C++ | `domains/ue5-cpp/` | Unreal Engine 5 plugin and systems development in C++ |
| Technical Design | `domains/technical-design/` | Design-engineering bridge work, prototyping, spec translation |

Each domain contains:
- `DOMAIN.md` — Scope, conventions, key concepts
- `agents/` — Specialized agent definitions
- `commands/` — Slash command definitions
- `prompts/` — Reference material and reusable knowledge bases

## Templates

Exportable project scaffolds live under `templates/`. These contain `.template` files that get renamed and variable-substituted when deployed.

| Template | Path | Purpose |
|----------|------|---------|
| UE5 Plugin | `templates/ue5-plugin/` | Bootstrap a new UE5 C++ plugin project |

Each template has a `TEMPLATE.md` explaining its contents and variables.

## References

| Reference | Path | Description |
|-----------|------|-------------|
| Claude Code Artifacts | `references/claude-code-artifacts.md` | Format specs for every artifact type: commands, agents, skills, hooks, settings, templates |

## Kit Commands

Two core commands manage this kit:

| Command | Purpose |
|---------|---------|
| `/extract` | Deploy kit content (templates, agents, commands, prompts) to a target project path |
| `/create` | Create new kit content (agents, commands, prompts, skills, hooks, domains, templates) |

## Extraction Workflow

The primary way to use this kit is the `/extract` command. It handles:
- Deploying a full template to a target path (e.g., "set up ue5-plugin at F:\Projects\MyNewPlugin")
- Copying specific agents, commands, or prompts to a target project's `.claude/` directory
- Installing a whole domain's tooling into an existing project

The command never overwrites existing files without confirmation. Template files (`.template` extension) get renamed and have `{{VARIABLE}}` placeholders substituted during extraction.

## Creation Workflow

Use `/create` (or just describe what you want) to add new content to the kit. The `/create` command follows the format specs in `references/claude-code-artifacts.md` and ensures every new artifact:

- Lands in the correct directory
- Follows the correct format (frontmatter for agents/skills, no frontmatter for commands/prompts)
- Meets the quality standards below
- Updates CLAUDE.md and README.md navigation tables when adding domains or templates

### What Goes Where

| You want to create... | It goes in... |
|----------------------|---------------|
| Agent (specialist role) | `domains/<domain>/agents/<name>.md` |
| Command (action/verb) | `domains/<domain>/commands/<name>.md` or `.claude/commands/<name>.md` (kit-level) |
| Prompt (reference knowledge) | `domains/<domain>/prompts/<name>.md` |
| Skill (knowledge bundle) | `.claude/skills/<name>/SKILL.md` |
| Hook (automatic trigger) | `.claude/settings.json` or `.claude/settings.local.json` |
| Domain (new specialty area) | `domains/<name>/` with DOMAIN.md + agents/ + commands/ + prompts/ |
| Template (project scaffold) | `templates/<name>/` with TEMPLATE.md + .template files |

### Artifact Format Quick Reference

| Type | Frontmatter | Key Fields | Special Markers |
|------|-------------|------------|-----------------|
| Command | None | — | `$ARGUMENTS` at end |
| Agent | YAML required | `agentName`, `description` | — |
| Skill | YAML required | `name`, `description` | SKILL.md entry point |
| Prompt | None | — | — |
| Hook | JSON in settings | event, matcher, command | — |
| Template files | None | — | `{{VARIABLE}}` placeholders, `.template` extension |

For complete format specifications with examples, see `references/claude-code-artifacts.md`.

## Quality Standards

When creating or modifying content in this kit:

1. **No placeholder content.** Every file must contain real, immediately useful material. An empty file with TODO comments is worse than no file.
2. **Opinionated over generic.** This kit reflects one person's workflow. Specificity is a feature. Write for someone who knows UE5's module system, understands 11ms frame budgets, and thinks in terms of interaction affordances.
3. **Agents are specialists, not generalists.** Each agent has a narrow, well-defined role. An agent that "helps with UE5" is useless. An agent that "reviews UE5 C++ classes for UFUNCTION/UPROPERTY macro correctness and memory safety" is useful.
4. **Commands are verbs.** Every command performs a specific action. `/review-ue5-class` produces a review. `/design-to-spec` produces a specification.
5. **Prompts are reference, not instruction.** Prompt files are knowledge bases that agents and commands pull from — not standalone instructions.
6. **Skills are expertise, not procedures.** Skills make Claude better at a class of work. They're knowledge bundles, not step-by-step instructions.
7. **Follow the format specs.** Every artifact type has a defined format in `references/claude-code-artifacts.md`. Don't improvise formats — follow the spec.

## Conventions

- All markdown files use ATX headers (`#` not `===`)
- File names are kebab-case
- Directory names are kebab-case
- Templates use `.template` extension for files that need variable substitution
- Template variables use `{{VARIABLE_NAME}}` syntax
- Domain agents/commands/prompts live under `domains/`, not under `.claude/`
- Root `.claude/commands/` contains only kit-management commands

## Working in This Kit

When asked to create new content:
- Read `references/claude-code-artifacts.md` for format specs before creating any artifact
- Read the relevant DOMAIN.md before adding content to a domain
- Use `/create` for guided creation, or create directly if you know the format
- After adding a domain or template, update the navigation tables in this file and README.md
- Maintain the quality standards above — every file must have real, substantive content

When asked to modify existing content:
- Read the file first to understand current content
- Maintain the existing format and style
- Don't broaden an agent's scope — keep specialists narrow

When asked to extract/install content to another project:
- Identify which domain(s) and/or template are relevant
- Use the extraction workflow described above
- Adapt file paths and variable values to the target project
