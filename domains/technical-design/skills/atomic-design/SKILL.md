---
name: atomic-design
description: >
  Build new UIs from scratch or refactor existing UIs using Brad Frost's Atomic Design methodology.
  Use this skill whenever the user mentions atomic design, design systems, component hierarchies,
  UI component architecture, or asks to organize/restructure/refactor UI components into a systematic
  hierarchy. Also trigger when the user wants to create a component library, establish a pattern library,
  break a monolithic UI into reusable parts, or audit an existing interface for consistency. Works with
  any language or framework — React, Vue, Angular, Svelte, Flutter, SwiftUI, Jetpack Compose, vanilla
  HTML/CSS, or any component-based UI system.
---

# Atomic Design Skill

Apply Brad Frost's Atomic Design methodology to build or refactor user interfaces as hierarchical,
composable component systems. This skill works in two modes — **Greenfield** (building new UIs from
scratch) and **Refactor** (restructuring existing UIs to conform to atomic principles). Both modes
produce the same outcome: a well-organized, five-level component hierarchy that maximizes reusability,
consistency, and scalability.

## Core Mental Model

Atomic Design decomposes every interface into five levels. These are not sequential build steps — they
are a way of seeing an interface as both a cohesive whole and a collection of composable parts
simultaneously. Think of it as a zoom lens: pages are the wide shot, atoms are the macro close-up,
and everything in between shows how parts compose into wholes.

**Atoms** → smallest meaningful UI elements (a button, an input, a label, an icon).
**Molecules** → small groups of atoms functioning as a single unit (a search field = label + input + button).
**Organisms** → complex sections composed of molecules and atoms (a site header = logo + nav + search).
**Templates** → page-level layouts that arrange organisms with placeholder content (the wireframe).
**Pages** → templates filled with real content, revealing edge cases and validating the system.

Before classifying components, read `classification-guide.md` for the decision framework
and worked examples that resolve common ambiguities (especially the molecule-vs-organism boundary).

## Detecting the Mode

Determine which mode applies based on the user's request and the state of the codebase.

**Greenfield mode** when any of these are true: the user says "build," "create," or "new"; there is
no existing component directory; the project is being initialized from scratch.

**Refactor mode** when any of these are true: the user says "refactor," "restructure," "reorganize,"
or "migrate"; there is an existing UI codebase with components that are not organized atomically;
the user asks for an "interface inventory" or "component audit."

If ambiguous, ask the user which mode they intend.

---

## Greenfield Mode — Building a New Atomic UI

### Step 1: Discover Context

Before writing any code, gather the following from the user (ask if not provided):

1. **Framework and language** — React/TSX, Vue/SFC, Svelte, Angular, Flutter, SwiftUI, vanilla HTML/CSS, etc.
2. **Styling approach** — CSS modules, Tailwind, styled-components, SCSS, design tokens, etc.
3. **Key screens or user journeys** — What are the 2–3 most important pages or flows?
4. **Brand foundations** — Do colors, typography, spacing values already exist? If so, these become the token/foundation layer beneath atoms.
5. **Existing design system** — Is there a Figma file, style guide, or design spec to reference?

### Step 2: Establish the Foundation Layer (Design Tokens)

Design tokens sit *beneath* atoms as a sub-atomic layer. They are the named constants that atoms
reference for all visual properties. Read `design-tokens.md` for full guidance.

Create a tokens/foundations file appropriate to the framework. At minimum define: color palette
(primary, secondary, neutral, semantic), typography scale (font families, sizes, weights, line heights),
spacing scale (consistent increments — e.g., 4px base), border radii, shadows/elevation, and
breakpoints. Every atom must reference tokens, never hard-coded values.

### Step 3: Build Atoms

Atoms are the irreducible UI elements. They should be stateless, purely presentational, and accept
all variation through props/parameters. Each atom must: reference tokens for all visual properties,
support all relevant states (default, hover, focus, disabled, error, loading), include accessibility
attributes (aria labels, roles, keyboard handling), and export a clean public API.

Common atoms: Button, Input, Label, Icon, Avatar, Badge, Divider, Spinner, Typography (Heading, Text),
Image, Link, Checkbox, Radio, Toggle, Tag/Chip, Tooltip (trigger only).

### Step 4: Compose Molecules

Molecules combine atoms into small, single-purpose functional units. A molecule should do one thing
and do it well. It should remain reusable across contexts — if it is only meaningful in one specific
organism, reconsider whether it should be a molecule or an internal part of that organism.

Common molecules: SearchField (label + input + button), FormField (label + input + error message),
NavItem (icon + label + link), MediaObject (image + text block), Card (image + heading + description),
Dropdown (button + option list), Breadcrumb (series of links + separators).

### Step 5: Assemble Organisms

Organisms are the first level with real contextual meaning. They form distinct interface sections.
Organisms define their own data contracts — they declare what data they need (via props/interfaces)
but do not fetch it themselves. Two varieties exist: heterogeneous organisms combine different
molecules (a header with logo, nav, and search) and homogeneous organisms repeat the same molecule
(a product grid of identical cards).

Common organisms: Header, Footer, Sidebar, HeroSection, ProductGrid, CommentThread, NavigationBar,
PricingTable, FeatureSection, LoginForm, RegistrationForm, DataTable.

### Step 6: Define Templates

Templates are layout skeletons that place organisms into a page structure using placeholder content.
They contain zero business logic and zero real data — only layout rules. Templates answer the
question: "Where does each organism go, and how do they relate spatially?" They are the bridge
between the component system and actual pages.

### Step 7: Instantiate Pages

Pages are specific instances of templates filled with real, representative content. They serve as the
ultimate validation of the system. For every page, test edge cases: what happens with empty states,
extremely long content, single items vs. many items, different user roles, loading states, and error
states. When a page reveals a problem, trace it back to the atom, molecule, or organism that needs
adjustment — do not patch at the page level.

### Step 8: Scaffold the Directory Structure

Use the framework-appropriate directory layout. For any framework, mirror the five levels:

```
src/
├── tokens/          (or foundations/, theme/)
│   ├── colors
│   ├── typography
│   ├── spacing
│   └── index
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   │   ├── Button.[ext]        ← component file
│   │   │   ├── Button.styles.[ext] ← styles (if separate)
│   │   │   ├── Button.test.[ext]   ← tests
│   │   │   ├── Button.stories.[ext]← docs (if using Storybook)
│   │   │   └── index.[ext]         ← clean re-export
│   │   ├── Input/
│   │   └── ...
│   ├── molecules/
│   │   ├── SearchField/
│   │   └── ...
│   ├── organisms/
│   │   ├── Header/
│   │   └── ...
│   └── templates/
│       ├── DashboardTemplate/
│       └── ...
├── pages/
│   ├── HomePage/
│   └── ...
└── index.[ext]      ← barrel export
```

Adapt file extensions and conventions to the framework (`.tsx`, `.vue`, `.svelte`, `.dart`, `.swift`,
`.kt`, etc.). For CSS-in-JS or utility-class approaches, the styles file may be unnecessary. The key
invariant is the five-level folder hierarchy with co-located component files.

---

## Refactor Mode — Restructuring an Existing UI

For refactoring existing codebases, read `refactoring-playbook.md` for the full
step-by-step process. The high-level workflow is:

### Step 1: Interface Inventory

Crawl the existing component/source directory. Catalog every UI element: buttons (how many unique
styles?), form inputs, navigation patterns, cards, modals, headers, footers, and any other recurring
pattern. Group them by visual function. This inventory makes inconsistencies visible — it is common
to find 5–10 variations of the same button across a codebase.

### Step 2: Classification

Using the decision framework in `classification-guide.md`, classify every discovered
element into atom, molecule, organism, template, or page. Produce a classification map that the user
can review before any code changes begin.

### Step 3: Consolidation

For each classification group, identify duplicates and near-duplicates. Propose a canonical version
of each component that covers all legitimate use cases through props/variants rather than through
separate implementations. This is where the biggest consistency gains happen.

### Step 4: Extraction and Migration

Extract consolidated components into the atomic directory structure. Update imports across the
codebase to point to the new canonical locations. Preserve all existing functionality — refactoring
must not change user-facing behavior. Run existing tests after each extraction to catch regressions.

### Step 5: Token Extraction

Identify hard-coded colors, font sizes, spacing values, and other visual constants throughout the
codebase. Extract them into a design tokens layer. Update all atoms to reference tokens instead of
literals. This enables future theming and ensures visual consistency.

### Step 6: Validation

After refactoring, verify: every component renders identically to its pre-refactor version (visual
regression testing), all existing tests pass, the new directory structure follows atomic conventions,
no circular dependencies exist between levels (atoms never import molecules, molecules never import
organisms), and components at each level are appropriately stateless or stateful.

---

## Composition Rules (Both Modes)

These rules govern how components at each level may reference components at other levels. They are
the structural backbone of Atomic Design and must never be violated.

1. **One-directional dependency flow.** Atoms depend on nothing (only tokens). Molecules depend on
   atoms. Organisms depend on molecules and/or atoms. Templates depend on organisms. Pages depend
   on templates. Never reverse this flow.

2. **Atoms and molecules are stateless and presentational.** They receive all data and callbacks via
   props. They contain no business logic, no data fetching, no side effects, and no global state access.

3. **Organisms define data contracts.** They declare the shape of data they need (via props, interfaces,
   or type definitions) but do not know where the data comes from.

4. **Templates are layout-only.** They contain no business logic, no data, and no content — only the
   spatial arrangement of organism slots.

5. **Pages are the integration point.** They are where data fetching, state management, routing, and
   real content converge. Pages may contain business logic.

6. **No level-skipping in the dependency chain.** A template should not directly use an atom. If a
   template needs a standalone button, that button should be wrapped in a molecule or placed within
   an organism. This ensures consistent composition and avoids fragmentation.

---

## Naming Conventions

Use clear, descriptive names that communicate purpose. Atoms and molecules should be generic and
reusable names (Button, SearchField). Organisms should describe their UI section role (SiteHeader,
ProductGrid). Templates should describe the page type they support (DashboardTemplate,
ArticleTemplate). Pages should describe the specific view (HomePage, ProductDetailPage, SettingsPage).

Prefix or suffix patterns vary by framework convention. In React: PascalCase component names. In Vue:
PascalCase or kebab-case per project style. In Angular: kebab-case with component suffix. Follow the
framework's idiomatic conventions but maintain the atomic folder hierarchy regardless.

---

## Accessibility at Every Level

Accessibility must be baked in at the atom level so it propagates automatically. Every interactive atom
must: have a visible focus indicator, support keyboard navigation, include appropriate ARIA attributes,
meet WCAG color contrast ratios (reference tokens for this), and support screen readers. Molecules
inherit atom accessibility but must also manage focus flow between their constituent atoms. Organisms
must manage focus trapping (for modals/dropdowns) and landmark roles. Audit at every level — issues
in atoms propagate system-wide.

---

## When Classification Is Ambiguous

If a component resists clean classification, apply this tiebreaker sequence:

1. Can it be broken down further without losing meaning? If no → atom. If yes → continue.
2. Does it do exactly one thing and combine 2–3 atoms? → molecule.
3. Does it form a distinct, recognizable section of an interface? → organism.
4. If still unclear, classify it as the *higher* level (prefer organism over molecule) and revisit
   after the system matures. Categorization debates should never block progress.

For the full decision tree with worked examples, read `classification-guide.md`.

---

## Quality Checklist

Before considering the atomic system complete, verify every item:

- [ ] Tokens layer exists and no component contains hard-coded visual values
- [ ] Every atom is stateless, presentational, and references only tokens
- [ ] Every molecule combines atoms and serves a single purpose
- [ ] Every organism defines its data contract via props/interfaces
- [ ] Templates contain only layout logic and placeholder slots
- [ ] Pages validate the system with real content and edge cases
- [ ] Dependency flow is strictly one-directional (atom → molecule → organism → template → page)
- [ ] No duplicate or near-duplicate components exist at any level
- [ ] Accessibility attributes are present at the atom level
- [ ] All components include state variants (default, hover, focus, disabled, error, loading, empty)
- [ ] Directory structure mirrors the five atomic levels with co-located files
- [ ] Barrel exports exist for clean imports from each level

---

## Further Reading

For specific deep-dive guidance, read the following reference files as needed:

- `classification-guide.md` — Full decision tree for classifying components, with worked
  examples covering the most common ambiguities (molecule vs. organism, where to put forms, how to
  handle compound components).
- `refactoring-playbook.md` — Detailed step-by-step process for migrating an existing
  codebase to atomic design, including interface inventory techniques, safe extraction patterns,
  and rollback strategies.
- `design-tokens.md` — How to structure the sub-atomic design token layer, including
  naming conventions, multi-theme support, platform-agnostic token formats, and integration with
  the atom layer.
