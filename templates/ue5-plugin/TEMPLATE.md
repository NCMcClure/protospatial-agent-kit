# UE5 Plugin Template

Bootstrap a new Unreal Engine 5 C++ plugin project with an agentic development workflow for Claude Code.

## Architecture

This template uses the **CLAUDE.md → @AGENTS.md delegation pattern** proven in the NodeToCode UE5 plugin:

- `CLAUDE.md` is a single-line file (`@AGENTS.md`) that delegates to the shared documentation
- `AGENTS.md` is the navigation hub — tracked in git, shared across the team
- `Context/` subdirectories provide deep, domain-specific documentation that agents load on demand
- `CLAUDE.md` is gitignored so each developer can personalize it without merge conflicts

This pattern scales: start with one Context/ directory (architecture) and add more as the project grows.

## What's Included

| File | Deployed As | Description |
|------|-------------|-------------|
| `CLAUDE.md.template` | `CLAUDE.md` | Single-line delegation to AGENTS.md (gitignored, local-only) |
| `AGENTS.md.template` | `AGENTS.md` | Navigation hub with UE source path, build info, conventions, context navigation |
| `Context/architecture/AGENTS-architecture.md.template` | `Context/architecture/AGENTS-architecture.md` | Plugin architecture: module structure, entry point, source org, logging |
| `.gitignore.template` | `.gitignore` | UE5-appropriate gitignore (includes CLAUDE.md as gitignored) |
| `.claude/settings.json.template` | `.claude/settings.json` | Shared project permissions (build script whitelist) |
| `.claude/commands/build-check.md` | `.claude/commands/build-check.md` | Command to verify project builds (supports multi-version build scripts) |
| `.claude/commands/find-ue-source.md` | `.claude/commands/find-ue-source.md` | Command to locate UE5 engine source and update AGENTS.md |

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{PROJECT_NAME}}` | Plugin/project name (PascalCase) | `NodeToCode`, `ProtoUI` |
| `{{UE_VERSION}}` | Target Unreal Engine version | `5.5`, `5.4` |
| `{{MODULE_NAME}}` | Primary module name (usually same as project name) | `NodeToCode` |
| `{{MODULE_TYPE}}` | Module type (Runtime or Editor) | `Editor` |
| `{{PROJECT_PREFIX}}` | Short class prefix for the project (2-4 chars) | `N2C`, `Proto`, `RMG` |

## Usage

From the Protospatial Agent Kit, use `/extract` and ask to deploy this template:

```
"Set up the ue5-plugin template at F:\Projects\MyNewPlugin with project name MyPlugin, prefix MP, targeting UE5.5 as an Editor module"
```

## After Deployment

1. Run `/find-ue-source` to detect and configure the UE5 engine source path in AGENTS.md
2. Update the Overview section in AGENTS.md with a description of your plugin
3. Begin development — the Claude configuration is ready to assist with UE5 C++ conventions

### Growing the Context Hierarchy

As your project develops, add more Context/ subdirectories for major subsystems:

```
Context/
├── architecture/                          ← included by template
│   └── AGENTS-architecture.md
├── your-subsystem/                        ← add as needed
│   └── AGENTS-your-subsystem.md
└── development-workflow/                  ← add as needed
    └── AGENTS-development-workflow.md
```

Update the Context Navigation and Quick Reference sections in AGENTS.md when adding new context files.

### Team Workflow

- **AGENTS.md** and **Context/** are git-tracked — shared knowledge that improves for everyone
- **CLAUDE.md** is gitignored — each developer can customize their local delegation (e.g., add personal notes, override with different agent config)
- **.claude/settings.json** is git-tracked — shared permissions and hooks
- **.claude/settings.local.json** is gitignored — personal permissions and MCP config
