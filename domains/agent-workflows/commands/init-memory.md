Initialize a progressive disclosure memory system in the current project or at a specified path.

If a path is provided as an argument, initialize the memory system there. Otherwise, initialize in the current working directory.

## Step 1: Determine Categories

Ask the user which memory categories they want. Present these defaults and let them customize:

**Default categories (recommended for most projects):**
- `project/` — Architecture decisions, roadmap, project overview
- `technical/` — Issues and solutions, environment setup, implementation learnings
- `creative/` — Design decisions, user preferences, domain-specific aesthetics

**Optional categories:**
- `people/` — Per-person context files (for projects with multiple stakeholders)
- `domain/` — Specialized domain knowledge, glossary, constraints
- `sessions/` — Auto-generated session logs (use sparingly — purpose-organized files are usually better)

If the user specifies categories in the arguments, use those directly without asking.

## Step 2: Create Directory Structure

Create the `memories/` directory with subdirectories for each chosen category.

## Step 3: Write the Index File

Create `memories/index.md` following this structure:

```markdown
# Memory System Index

## Navigation Principle: Progressive Disclosure
Start with this index. Read Quick Summaries in relevant directories.
Dive into full content only when needed for the current task.

## Directories

### <category>/
<one-sentence description of what knowledge lives here>
- `<file>.md` — <one-sentence description>
- `<file>.md` — <one-sentence description>

## Update Guidelines
1. Keep Quick Summaries current — they're the first thing readers see
2. Add timestamps to significant updates
3. Cross-reference related files across directories
4. Remove stale information rather than letting it accumulate
```

Use the category descriptions from the progressive-disclosure skill. Tailor the file list to the project's actual needs.

## Step 4: Create Starter Files

For each category, create the standard files with Quick Summary headers and format guidance. Every file must have real structure — not empty placeholder content.

**Example starter file for `technical/issues-solutions.md`:**

```markdown
# Technical Issues and Solutions

## Quick Summary
No issues recorded yet. This file captures problems encountered during implementation and their solutions.

## Entry Format
Each entry follows this structure:

### <Issue Title> (<YYYY-MM>)
- **Problem:** What went wrong or was unexpected
- **Root Cause:** Why it happened
- **Solution:** What fixed it
- **Related:** Cross-references to other memory files
```

Create similar starter files for every file listed in the index. Match the structure to the category — project files get overview/architecture/roadmap structures, creative files get decision-record structures.

## Step 5: Install Hooks (Optional)

Ask the user if they want to install the memory capture hooks. If yes:

1. Create `.claude/hooks/` directory if it doesn't exist
2. Write the stop hook script to `.claude/hooks/memory_capture_stop.py` (from the memory-capture-stop hook reference in this domain)
3. Write the session start hook to `.claude/hooks/memory_context_start.py` (from the memory-context-start hook reference in this domain)
4. Create or update `.claude/settings.local.json` to include the hook configuration:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/memory_capture_stop.py",
            "timeout": 60
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/memory_context_start.py"
          }
        ]
      }
    ]
  }
}
```

If `.claude/settings.local.json` already exists with other hooks, merge the new entries alongside existing ones.

## Step 6: Generate Config (Optional)

If custom categories were chosen, create `memory_config.json` in the project root with routing configuration:

```json
{
  "memory_dir": "memories",
  "meaningful_keywords": [
    "implemented", "fixed", "created", "updated", "refactored",
    "discovered", "learned", "solution", "approach", "decision",
    "resolved", "analyzed", "debugged", "designed", "architected",
    "chose", "migrated", "optimized", "integrated"
  ],
  "routing": {
    "<category>": ["<keywords>", "..."],
    "<category>": ["<keywords>", "..."]
  }
}
```

Map keywords to categories based on the project's domain. If using only the default categories, this file is optional — the stop hook uses sensible defaults.

## Output

After initialization, report:
- Total directories created
- Total files created
- Whether hooks were installed
- The path to `memories/index.md` as the entry point
- Remind the user to add `memories/` to their `.gitignore` if they don't want memory committed, or to commit it if they do

$ARGUMENTS
