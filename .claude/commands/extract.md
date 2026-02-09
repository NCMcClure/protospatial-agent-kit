Extract and install content from the Protospatial Agent Kit to a target project.

The user will tell you what they need and where. Determine which of these extraction modes applies:

## Mode 1: Template Deployment

If the user wants to set up a new project from a template:

1. List available templates from `templates/` (read each `TEMPLATE.md` for descriptions)
2. Confirm which template and the target directory path
3. Ask for template variable values (read the TEMPLATE.md to know which variables are needed)
4. For each file in the template directory:
   - Skip `TEMPLATE.md` (it's documentation, not deployed)
   - Files ending in `.template`: copy to target with the `.template` extension removed, and replace all `{{VARIABLE_NAME}}` placeholders with the user's values
   - All other files (e.g., `.claude/commands/*.md`): copy as-is to the matching path in the target
5. NEVER overwrite existing files without explicit confirmation
6. Report every file created with its full path

## Mode 2: Specific Asset Extraction

If the user wants specific agents, commands, or prompts copied to an existing project:

1. Identify the requested assets (e.g., "the code reviewer agent", "design-to-spec command")
2. Locate them under `domains/`
3. Determine the correct target path:
   - Agents → `<target>/.claude/agents/`
   - Commands → `<target>/.claude/commands/`
   - Prompts → copy to a location the user specifies (prompts are reference material, not Claude Code config)
4. Copy the files, creating directories as needed
5. NEVER overwrite existing files without explicit confirmation
6. Report what was installed

## Mode 3: Domain Tooling Installation

If the user wants an entire domain's tooling installed:

1. Read the domain's `DOMAIN.md` to understand what's available
2. List all agents, commands, and prompts in the domain
3. Confirm what the user wants (all of it, or a subset)
4. Copy to the target project following Mode 2 path conventions
5. Suggest the user review copied agents/commands to customize them for their specific project

## Mode 4: Inventory

If the user asks what's available (or you need to show options):

1. Walk `domains/` and `templates/` directories
2. For each domain: list agents, commands, and prompts with one-line descriptions (read the first few lines of each file)
3. For each template: read TEMPLATE.md for the summary
4. Present as a concise inventory table

$ARGUMENTS
