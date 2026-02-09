# UE5 Plugin Template

Bootstrap a new Unreal Engine 5 C++ plugin project with Claude Code configuration.

## What's Included

| File | Deployed As | Description |
|------|-------------|-------------|
| `CLAUDE.md.template` | `CLAUDE.md` | Project-level Claude instructions with UE5 conventions, module structure, and workflow guidance |
| `.gitignore.template` | `.gitignore` | UE5-appropriate gitignore covering build artifacts, IDE files, and Claude Code local settings |
| `.claude/commands/build-check.md` | `.claude/commands/build-check.md` | Command to verify project builds successfully |
| `.claude/commands/find-ue-source.md` | `.claude/commands/find-ue-source.md` | Command to locate UE5 engine source installation |

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{PROJECT_NAME}}` | Plugin/project name (PascalCase) | `NodeToCode`, `ProtoUI` |
| `{{UE_VERSION}}` | Target Unreal Engine version | `5.5`, `5.4` |
| `{{MODULE_NAME}}` | Primary module name (usually same as project name) | `NodeToCode` |
| `{{MODULE_TYPE}}` | Module type (Runtime or Editor) | `Editor` |

## Usage

From the Protospatial Agent Kit, use `/extract` and ask to deploy this template:

```
"Set up the ue5-plugin template at F:\Projects\MyNewPlugin with project name MyPlugin targeting UE5.5"
```

After deployment:
1. Review the generated `CLAUDE.md` and customize the project description and module structure sections
2. Run `/find-ue-source` to detect and configure the UE5 engine source path
3. Begin development — the Claude configuration is ready to assist with UE5 C++ conventions
