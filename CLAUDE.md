# Protospatial Agent Kit

## Identity

You are operating inside a personal agent toolkit owned by a senior XR/ML technical designer who bridges design and engineering. This kit is not a project to be built — it is a living reference system that grows organically as useful patterns, agents, commands, and prompts are identified through real daily work.

Your role when operating in this kit is to help the user find, deploy, and maintain its contents. The user will clone this repo to any machine, open Claude Code in it, and ask you to extract or install specific pieces into target project paths.

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

## Extraction Workflow

The primary way to use this kit is the `/extract` command. It handles:
- Deploying a full template to a target path (e.g., "set up ue5-plugin at F:\Projects\MyNewPlugin")
- Copying specific agents, commands, or prompts to a target project's `.claude/` directory
- Installing a whole domain's tooling into an existing project

The command never overwrites existing files without confirmation. Template files (`.template` extension) get renamed and have `{{VARIABLE}}` placeholders substituted during extraction.

## Quality Standards

When creating or modifying content in this kit:

1. **No placeholder content.** Every file must contain real, immediately useful material. An empty file with TODO comments is worse than no file.
2. **Opinionated over generic.** This kit reflects one person's workflow. Specificity is a feature. Write for someone who knows UE5's module system, understands 11ms frame budgets, and thinks in terms of interaction affordances.
3. **Agents are specialists, not generalists.** Each agent has a narrow, well-defined role. An agent that "helps with UE5" is useless. An agent that "reviews UE5 C++ classes for UFUNCTION/UPROPERTY macro correctness and memory safety" is useful.
4. **Commands are verbs.** Every command performs a specific action. `/review-ue5-class` produces a review. `/design-to-spec` produces a specification.
5. **Prompts are reference, not instruction.** Prompt files are knowledge bases that agents and commands pull from — not standalone instructions.

## Conventions

- All markdown files use ATX headers (`#` not `===`)
- File names are kebab-case
- Directory names are kebab-case
- Templates use `.template` extension for files that need variable substitution
- Template variables use `{{VARIABLE_NAME}}` syntax
- Domain agents/commands/prompts live under `domains/`, not under `.claude/`
- Root `.claude/commands/` contains only kit-management commands

## Working in This Kit

When asked to modify kit content:
- Read the relevant DOMAIN.md before touching domain content
- Maintain the quality standards above
- New domains follow the existing structure: DOMAIN.md + agents/ + commands/ + prompts/

When asked to extract/install content to another project:
- Identify which domain(s) and/or template are relevant
- Use the extraction workflow described above
- Adapt file paths and variable values to the target project
