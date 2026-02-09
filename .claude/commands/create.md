Create a new artifact in the Protospatial Agent Kit.

**Important**: Everything created by this command is portable content stored under `domains/` or `templates/`. These artifacts exist to be extracted and deployed into other projects via `/extract`. Do NOT create anything in this kit's own `.claude/` directory — that path is reserved for kit management commands only.

Read `references/claude-code-artifacts.md` for the exact format specifications of each artifact type. All artifacts created must follow those formats precisely.

Determine what the user wants to create based on their request. If unclear, ask.

## Importing From an Existing Project

If the user provides a file path as an argument (e.g., `/create F:\Projects\NodeToCode\.claude\commands\build-check.md`), they want to **import an existing artifact from another project into this kit**:

1. Read the file at the provided path
2. Determine what type of artifact it is (command, agent, skill, prompt, hook, etc.) based on its format and location
3. Ask which domain it belongs to in this kit
4. Adapt the content if needed to be portable and kit-appropriate (remove project-specific hardcoded paths, generalize where sensible while preserving the useful specifics)
5. Write it to the correct location under `domains/<domain>/` following the format specs
6. Summarize what was imported and what was adapted

If the path points to a directory (e.g., a skill directory with SKILL.md + supporting files), import the entire directory.

## Creating a Command

Target: `domains/<domain>/commands/<name>.md`

1. Ask which domain this belongs to
2. Ask for the command name (will be kebab-cased)
3. Ask what the command should do — what verb does it perform, what output does it produce?
4. Write the command file following the format in the artifact reference:
   - No frontmatter
   - Imperative instructions to Claude
   - Structured output specification
   - `$ARGUMENTS` at end if it accepts input
5. Verify: Does this command produce a specific output? If it's conversational rather than productive, redesign it as a verb.

## Creating an Agent

Target: `domains/<domain>/agents/<name>.md`

1. Ask which domain this belongs to
2. Ask for the agent name (will be kebab-cased) and one-line description
3. Ask what this agent specializes in — what is its narrow scope?
4. Ask what its output format should look like
5. Write the agent file:
   - YAML frontmatter with `agentName` and `description`
   - "You are a..." role framing
   - Detailed process/checklist
   - Structured output format
   - Quality standards
6. Verify: Is the scope narrow enough? An agent that "helps with X" is too broad. An agent that "reviews X for Y and Z" is right.

## Creating a Prompt

Target: `domains/<domain>/prompts/<name>.md`

1. Ask which domain this belongs to
2. Ask what knowledge this prompt should contain
3. Write the prompt file:
   - No frontmatter
   - Dense reference content (tables, decision trees, examples)
   - Organized by concept, not by instruction
4. Verify: Is this reference material or instructions? If it reads like "do this, then do that" it should be a command or agent, not a prompt.

## Creating a Skill

Target: `domains/<domain>/skills/<name>/SKILL.md` (plus optional supporting files in the same directory)

1. Ask which domain this belongs to
2. Ask for the skill name and description
3. Ask what knowledge or capability this skill provides
4. Create the skill directory and SKILL.md:
   - YAML frontmatter with `name` and `description`
   - Core knowledge organized by section
   - References to any supporting files
5. If the skill needs supporting reference files, create them in the same directory
6. Verify: Does this make Claude better at a CLASS of work, or is it a one-off instruction? Skills are expertise, not procedures.

When extracted, skills get deployed to `<target>/.claude/skills/<name>/`.

## Creating a Hook

Target: `domains/<domain>/hooks/<name>.md`

Hook definitions are stored as documented patterns — a markdown file describing the hook's purpose, event, matcher, and command — so they can be reviewed before installation.

1. Ask which domain this belongs to
2. Ask what event should trigger the hook (PreToolUse, PostToolUse, Notification, Stop)
3. Ask what tool matcher to use (or empty for all tools)
4. Ask what shell command should run
5. Write a hook definition file containing:
   - Purpose description
   - The JSON snippet to add to a project's `.claude/settings.json`
   - Installation instructions
6. Verify: Is this hook fast? Slow hooks block Claude's workflow.

When extracted, the `/extract` command merges hook JSON into the target project's settings file.

## Creating a Domain

Target: `domains/<name>/`

1. Ask for the domain name, display name, and scope description
2. Ask for 3-5 key concepts within the domain
3. Ask what's explicitly OUT of scope
4. Ask about cross-domain connections
5. Create the directory structure:
   ```
   domains/<name>/
     DOMAIN.md
     agents/
     commands/
     prompts/
   ```
6. Write DOMAIN.md with sections: Scope (In Scope + Out of Scope), Key Concepts, Conventions, Cross-Domain Connections
7. Update the root CLAUDE.md domain navigation table to include the new domain
8. Update README.md to include the new domain in the overview table

## Creating a Template

Target: `templates/<name>/`

Templates ARE portable project scaffolds, so they contain `.claude/` structure that gets deployed to the target project.

1. Ask for the template name and what kind of project it bootstraps
2. Ask what template variables are needed (e.g., `{{PROJECT_NAME}}`)
3. Ask what commands, skills, or hooks the template should include
4. Create the directory structure:
   ```
   templates/<name>/
     TEMPLATE.md
     CLAUDE.md.template
     .gitignore.template
     .claude/
       commands/
       skills/       (if needed)
       settings.json (if hooks are included)
   ```
5. Write TEMPLATE.md documenting the template, variables, and usage
6. Write CLAUDE.md.template with variable placeholders and project-appropriate sections
7. Write .gitignore.template appropriate for the project type
8. Write any included commands, skills, or hook configurations
9. Update the root CLAUDE.md template table
10. Update README.md template table

## After Creation

After creating any artifact:
1. Read it back and verify it follows the format spec in `references/claude-code-artifacts.md`
2. Confirm the file was written to the correct location under `domains/` or `templates/`
3. Summarize what was created and how to extract/deploy it with `/extract`

$ARGUMENTS
