# Refactoring Playbook: Migrating an Existing UI to Atomic Design

This reference provides the complete step-by-step process for restructuring an existing codebase
to conform to atomic design principles. The goal is to achieve atomic organization without
changing any user-facing behavior — this is a structural refactor, not a redesign.

## Before You Start

### Prerequisites

Ensure these conditions are met before beginning the refactor:

The project has a working test suite (unit tests, integration tests, or visual regression tests).
If it does not, write at minimum a visual snapshot or screenshot test for every major page before
making structural changes. These tests are your safety net — they prove the refactor did not
break anything.

The team agrees on the target framework conventions (naming, file structure, styling approach).
Atomic Design is framework-agnostic but the implementation details matter. Decide upfront whether
components will use CSS modules, Tailwind, styled-components, SCSS, or another approach, and
whether you will adopt Storybook or another documentation tool.

You have identified a pilot scope. Do not attempt to refactor the entire codebase at once. Pick
one critical user journey (e.g., the product detail page, the checkout flow, or the dashboard)
and refactor that first. Use it as a proof of concept before expanding.

---

## Phase 1: Interface Inventory

The interface inventory is the diagnostic step. It reveals the true state of the existing UI
by surfacing every unique visual pattern in the codebase.

### Step 1.1: Crawl the Source

Scan the existing component/source directory. For each file, record: the component name, its
file path, a brief description of what it renders, and an estimated complexity (simple, medium,
complex). Produce a flat list of every component.

If the codebase has no component structure (e.g., it is a monolithic template file or a series
of page-level files with inline HTML), scan by visual region instead: header, footer, sidebar,
main content area, modals, forms, navigation, cards, buttons, inputs, etc.

### Step 1.2: Screenshot Inventory

For every unique UI pattern — not every component, but every visually distinct element — capture
a representative example. Group screenshots by category: all buttons together, all form inputs
together, all card variants together, all navigation patterns together.

This visual grouping makes inconsistencies viscerally obvious. It is common to discover 5–15
unique button styles in a medium-sized codebase, most of which should be consolidated into 2–3
button variants.

### Step 1.3: Document the Inventory

Produce an inventory document (a markdown file or spreadsheet) with the following columns for
each pattern:

| Pattern | File(s) | Category | Variations | Notes |
|---------|---------|----------|------------|-------|
| Primary Button | Button.tsx, actions.css | Atom | 4 visual variants across codebase | Consolidate to 1 component with props |
| Search Bar | Header.tsx (inline), SearchPage.tsx (separate) | Molecule | 2 implementations | Extract shared molecule |
| Product Card | ProductList.tsx, RelatedProducts.tsx | Organism | 3 layouts (grid, list, compact) | Unify with layout prop |
| ... | ... | ... | ... | ... |

The "Category" column uses the atomic classification from `classification-guide.md`. The
"Variations" column captures how many distinct implementations of the same conceptual pattern
exist. The "Notes" column suggests the consolidation strategy.

Present this inventory to the user for review before proceeding. They may have context about
why certain variations exist (intentional vs. accidental) and which patterns are slated for
removal.

---

## Phase 2: Classification and Consolidation Plan

### Step 2.1: Classify Every Pattern

Using the decision tree in `classification-guide.md`, assign each inventory item to one of the
five atomic levels. For ambiguous items, document the reasoning and apply the tiebreaker heuristics.

Group the classified patterns by level:

**Atoms identified:** [list with brief description]
**Molecules identified:** [list showing which atoms they compose]
**Organisms identified:** [list showing which molecules/atoms they compose]
**Templates identified:** [list of page layouts]
**Pages identified:** [list of specific pages]

### Step 2.2: Design the Consolidation Plan

For each group of related patterns (e.g., the 4 different button implementations), propose a
canonical component that handles all legitimate use cases through props or variants. Document:

The canonical component name and its API (props/parameters). Which existing implementations it
replaces. What prop values map to each existing variation. Whether any existing variation should
be dropped entirely (deprecated patterns). Any new variants needed that do not exist yet.

### Step 2.3: Map the Dependency Graph

Before extracting anything, map the dependency relationships between the proposed components.
Verify that the dependency graph follows the one-directional flow: atoms → molecules → organisms
→ templates → pages. If circular dependencies exist in the current codebase, plan how to break
them.

Common circular dependency patterns and how to resolve them:

**Organism imports an atom that imports the organism** — The atom likely has too much
responsibility. Extract the shared logic into a utility or move the dependency to a higher level.

**Two organisms import each other** — One should be decomposed into molecules that both organisms
can share, or the shared part should be extracted into a new organism that both reference.

**Page-level logic leaked into a molecule** — Move the logic to the page or organism level and
pass the result down as props.

---

## Phase 3: Directory Scaffolding

### Step 3.1: Create the Atomic Directory Structure

Without moving any existing code, create the target directory structure alongside the existing one:

```
src/
├── components/           ← existing (untouched initially)
│   ├── Header.tsx
│   ├── Button.tsx
│   └── ...
├── atomic/               ← new (target structure)
│   ├── tokens/
│   ├── atoms/
│   ├── molecules/
│   ├── organisms/
│   └── templates/
└── pages/
```

Using a parallel directory (`atomic/` alongside `components/`) allows incremental migration. The
existing `components/` directory continues to work while you extract components one by one into
the new structure. Once migration is complete, the old directory is removed.

### Step 3.2: Create Barrel Exports

Set up index files at each level so that consumers can import from clean paths:

```
import { Button, Input, Icon } from '@/atomic/atoms'
import { SearchField, FormField } from '@/atomic/molecules'
import { Header, Footer } from '@/atomic/organisms'
```

These barrel exports should re-export every public component at each level. They also serve as
an inventory of the atomic system at a glance.

---

## Phase 4: Extraction (Bottom-Up)

Extract components starting from atoms and working up. This ensures that when you build molecules,
the atoms they depend on are already in place.

### Step 4.1: Extract Tokens

Scan the entire codebase for hard-coded color values, font sizes, spacing values, border radii,
shadows, and breakpoints. Create a tokens file that captures every unique value. Consolidate near-
duplicates (e.g., `#333333` and `#343434` are probably the same intended color).

After creating tokens, do NOT yet update existing components. Just create the token definitions.
They will be consumed as atoms are extracted.

### Step 4.2: Extract Atoms

For each atom in the consolidation plan:

1. Create the canonical component in `atomic/atoms/[ComponentName]/`.
2. Implement it using tokens for all visual properties.
3. Ensure it supports all identified state variants (default, hover, disabled, etc.).
4. Add accessibility attributes.
5. Write unit tests that cover all variants.
6. Create a migration alias — a re-export from the old location that points to the new component,
   preserving backward compatibility:

```typescript
// Old location: components/Button.tsx (becomes a thin re-export)
export { Button } from '@/atomic/atoms/Button'
// With prop mapping if the API changed:
export const OldButton = (props) => <Button variant={mapOldVariant(props.type)} {...props} />
```

This alias strategy allows gradual migration. Every file that imported the old Button continues
to work, but is now secretly using the new atomic Button.

### Step 4.3: Extract Molecules

For each molecule, create it in `atomic/molecules/` composing the already-extracted atoms. Follow
the same alias strategy for backward compatibility.

### Step 4.4: Extract Organisms

For each organism, create it in `atomic/organisms/` composing extracted molecules and atoms. This
is where the most significant code changes happen — organisms in the old codebase often contain
inline atoms and molecules that have now been extracted. The organism should import from the atomic
levels below it rather than reimplementing those elements.

### Step 4.5: Extract Templates

Create layout templates in `atomic/templates/`. These should contain only the spatial arrangement
of organism slots with no real content or business logic.

### Step 4.6: Wire Up Pages

Update pages to use the new templates and organisms. Pages are the integration point where data
fetching, routing, and state management live.

---

## Phase 5: Cleanup

### Step 5.1: Update All Imports

Once all components are extracted and aliases are in place, systematically update every import
in the codebase to point directly to the new atomic locations (removing the aliases). Do this
file by file, running tests after each batch of updates.

### Step 5.2: Remove Old Directory

Once no file imports from the old `components/` directory, remove it. This is the final step —
the codebase now has a clean atomic structure.

### Step 5.3: Run Full Test Suite

Execute all unit tests, integration tests, and visual regression tests. Every test should pass
with no changes to expected output. If any test fails, the refactor introduced a behavioral
change — fix it before considering the refactor complete.

### Step 5.4: Document the System

Produce documentation for the new atomic system: a component catalog (ideally in Storybook or
an equivalent tool), usage guidelines for each level, contribution guidelines explaining how to
classify new components, and a decision log explaining significant classification choices.

---

## Rollback Strategy

At every phase, the codebase should be in a working state. If a problem is discovered at any
point, the rollback strategy is:

During Phase 3 (scaffolding): Simply delete the empty `atomic/` directory. Zero impact.

During Phase 4 (extraction): Every extracted component has an alias at its old location. Consumers
are unaffected. To roll back, delete the `atomic/` directory and remove the aliases — the old
components are still in place.

During Phase 5 (cleanup): If imports have been updated but tests fail, revert the import changes
(restore the aliases). The atomic components themselves remain in place.

This incremental approach means you can stop the refactor at any point and the codebase remains
functional. There is never a "big bang" moment where everything changes at once.

---

## Handling Special Cases

### Server Components and Client Components (Next.js, Remix, etc.)

In frameworks that distinguish server and client components, the atomic classification still
applies. Atoms and molecules are typically client components (they handle interactivity). Some
organisms may be server components if they only display data. Templates and pages follow the
framework's routing and rendering conventions. Add a clear comment or naming convention to
distinguish server from client components within the atomic hierarchy.

### Shared Components Across Micro-Frontends

If the product consists of multiple independently deployed applications, extract the shared atoms
and molecules into a published package (npm, internal registry, etc.) that all applications consume.
Organisms and above typically remain application-specific because they encode application-specific
data contracts.

### Mobile Components (Flutter, SwiftUI, Jetpack Compose)

The atomic hierarchy applies identically. The directory structure uses framework-appropriate
conventions (e.g., `.dart` files for Flutter, `.swift` for SwiftUI). The key difference is
that mobile components may need platform-specific atoms (iOS-styled button vs. Material button)
that share the same molecule composition. Handle this through a platform token layer that atoms
reference.

### Legacy Codebases Without Components

If the codebase uses server-rendered templates (PHP, Django, Rails ERB, Jinja) with no component
abstraction, the refactor starts by identifying repeating HTML patterns and extracting them into
partial templates or includes. The atomic hierarchy maps onto the template inclusion system: atoms
are the smallest partials, molecules compose atom partials, and so on. The token layer maps onto
CSS variables or preprocessor variables.
