---
name: ue-slate-ui
description: >
  Build new UE5 Slate UIs from scratch or refactor existing Slate widget hierarchies using
  an atomic design methodology adapted for Slate's C++ composition model. Use this skill when
  the user mentions Slate UI, SWidget, SCompoundWidget, widget hierarchy, Slate refactoring,
  Slate design system, widget composition, or asks to organize/restructure Slate widgets into
  a systematic hierarchy. Also trigger when the user wants to create a Slate component library,
  establish a Slate style system, break a monolithic SCompoundWidget into reusable parts, or
  audit an existing Slate interface for consistency. Works for both editor tools (detail
  customizations, asset editors, standalone windows) and runtime Slate UIs.
---

# UE5 Slate UI

An architecture methodology for UE5 Slate UIs that applies atomic design principles to Slate's C++ composition model. Widgets are organized into five levels with strict dependency flow, styled through a centralized token and style set system, and connected through Slate's delegate and TAttribute patterns.

Two operating modes: **Greenfield** (building a new Slate UI from scratch) and **Refactor** (restructuring an existing Slate widget hierarchy into the five-level system).

## Core Mental Model

The five-level hierarchy maps atomic design to Slate-native concepts. The levels are renamed to match how Slate developers think — "Primitive" resonates where "Atom" doesn't, "Composite" is more precise than "Organism" for a widget that composes a recognizable UI section.

| Level | Atomic Equivalent | Slate Construct | Contains | Example |
|-------|-------------------|-----------------|----------|---------|
| **Primitive** | Atom | Single-purpose `SCompoundWidget` wrapping 1-2 native elements | Only tokens and style set references | Styled panel, icon button, styled separator |
| **Component** | Molecule | `SCompoundWidget` composing 2-4 Primitives | Primitives for a single micro-task | Header bar, labeled field, search bar |
| **Composite** | Organism | `SCompoundWidget` with data contract | Components, Primitives, other Composites | Filterable list view, toolbar, property panel |
| **Layout** | Template | SSplitter / SDockTab / SOverlay skeleton | Composite slots, no business logic | Main window skeleton, two-pane editor layout |
| **View** | Page | Top-level widget with subsystem access | Populated Layout wired to real data | The actual tool window, settings panel |

Think of the levels as a zoom lens. Primitives are the closest zoom — a single styled border. Views are the widest — the entire tool window with live data flowing through every Composite down to every Primitive.

## Core Principles

**One-directional dependency flow.** Primitives depend on nothing (only the token layer). Components compose Primitives. Composites compose Components and Primitives. Layouts arrange Composites. Views populate Layouts with data. Dependencies flow downward only — a Primitive never knows about the Component that contains it.

**Composition over inheritance.** Slate already favors composition (`SCompoundWidget` + `ChildSlot`). Deep `SWidget` inheritance hierarchies are an anti-pattern. When you need visual variants (a button that can be solid, transparent, or invisible), use a variant enum on a single widget class — not three subclasses. See `style-architecture.md`.

**Reactive styling through tokens.** All visual properties flow from a design token layer: constexpr spacing and sizing values, `FSlateFontInfo` factories, and a semantic color struct with reactive binding. No widget's `Construct` contains a hardcoded `FLinearColor`, font size, or spacing value. See `slate-design-tokens.md`.

**Delegate-driven communication.** Parent-child communication uses `SLATE_EVENT` delegates. Children fire events upward. Parents never reach into children. Widgets declare their events in `SLATE_BEGIN_ARGS` — this is their public API.

**TAttribute for dynamism.** Any property that changes at runtime (text, visibility, color, enabled state) uses `TAttribute` binding. Slate polls these every frame. This is how the UI stays reactive without explicit refresh calls.

**Stable address styling.** `FSlateBrush` and `FButtonStyle` instances live as static or member data with stable memory addresses. Slate holds `const FSlateBrush*` pointers — if the brush goes out of scope, Slate crashes. The `FSlateStyleSet` pattern centralizes all style instances with guaranteed lifetime. See `style-architecture.md`.

## Detecting the Mode

**Greenfield** when:
- Building a new tool, panel, or window from scratch
- No existing Slate widgets in the target area
- User says "create," "build," "new," "implement"

**Refactor** when:
- Existing `SCompoundWidget` hierarchy needs restructuring
- Monolithic `Construct` methods with hundreds of lines of inline `SNew`
- User says "refactor," "restructure," "extract," "decompose," "clean up"
- Existing Slate code works but is hard to maintain, extend, or understand

If ambiguous, ask the user. The two modes share the same destination (five-level hierarchy) but take different paths.

## Greenfield Mode

Seven steps to build a new Slate UI from the foundation up.

### Step 1: Discover Context

Gather from the user:
- **Target**: Editor tool or runtime UI? Standalone window, SDockTab, detail customization, or SOverlay HUD?
- **Modules**: What UE5 modules are available? (Slate, SlateCore, EditorStyle, ToolMenus, UMG)
- **Workflows**: What are the 2-3 primary user workflows this UI supports?
- **Settings**: Does a `UDeveloperSettings` exist for user-configurable values? Should one be created?
- **Existing styles**: Are there existing `FSlateStyleSet` instances to integrate with?
- **Project prefix**: What prefix for class names? (e.g., `My` → `SMyPanel`, `FMySlateStyle`)

### Step 2: Establish the Token Layer

Create the design token foundation. See `slate-design-tokens.md` for complete patterns.

**Produce:**
- `F[Prefix]Spacing` namespace — constexpr spacing scale (XXS through XXXL)
- `F[Prefix]Sizing` namespace — icon sizes, widget dimensions, border widths
- `F[Prefix]Fonts` namespace — `FSlateFontInfo` factory functions
- `F[Prefix]Colors` struct — semantic color members with UIBind reactive pattern

The token layer has zero dependencies on any widget code. It is pure data.

### Step 3: Build the Style Set

Create the centralized `FSlateStyleSet` subclass. See `style-architecture.md` for complete patterns.

**Produce:**
- `F[Prefix]SlateStyle` class with static brush and style members
- Variant enums (`E[Prefix]ButtonVariant`, `E[Prefix]PanelVariant`)
- `Initialize()` / `Shutdown()` lifecycle wired to module startup/shutdown
- `UpdateStyles()` wired to settings change delegate

### Step 4: Build Primitives

Each Primitive is a single-purpose `SCompoundWidget` or `SLeafWidget`. It references only the token layer and style set.

**Common Primitives to consider:**
- **Styled panel** — `SBorder` with variant enum (Light, Dark, Overlay) selecting brush from style set
- **Icon button** — `SButton` with `SImage` + optional `STextBlock`, variant-driven style (Standard, Simple, NoBorder)
- **Styled separator** — `SSeparator` with token-driven color and thickness
- **Styled checkbox** — `SCheckBox` with custom style from style set
- **Circular progress** — `SLeafWidget` with custom `OnPaint` for specialized visualization

**Each Primitive must:**
- Use `SLATE_BEGIN_ARGS` with appropriate arguments, attributes, and events
- Reference tokens for all visual properties — no hardcoded values
- Support all relevant states through variant enums, not subclasses
- Be completely stateless — receive all data via construction arguments and TAttribute bindings

### Step 5: Compose Components

Components combine 2-4 Primitives for a single purpose.

**Common Components to consider:**
- **Header bar** — panel + title text + optional close button
- **Labeled field** — label text + input widget
- **Search bar** — text input + search/clear icon button
- **Toolbar button group** — row of icon buttons with separator
- **Status indicator** — icon + text with color binding

**Each Component must:**
- Describe its purpose in one sentence without "and"
- Compose only Primitives (never Composites or Layouts)
- Have no domain-specific data contract — simple pass-through delegates at most

### Step 6: Assemble Composites

Composites form recognizable UI sections. They define data contracts via `SLATE_EVENT` delegates and `TAttribute` bindings.

**Common Composites to consider:**
- **Filterable list view** — `SListView` + `SHeaderRow` + search bar Component + `OnGenerateRow`
- **Property panel** — `SScrollBox` of labeled field Components with change delegates
- **Toolbar** — button group Components + dropdown menus + context label
- **Tree view panel** — `STreeView` + `OnGetChildren` + `OnSelectionChanged`
- **Detail section** — collapsible header Component + content area

**Each Composite must:**
- Define its data contract through SLATE_EVENT delegates — what events does it fire?
- Accept data through SLATE_ATTRIBUTE bindings — what data does it display?
- Not access subsystems or global singletons — data flows in through the contract
- Handle internal state (selection, filtering, expansion) without external coordination

See `composition-patterns.md` for `SListView`, `SOverlay`, and delegate patterns.

### Step 7: Define Layouts and Views

**Layouts** use `SSplitter`, `SDockTab`, `SOverlay` to arrange Composites into spatial regions. They accept Composites through named slots and contain zero business logic.

**Views** wire Layouts to real data. They:
- Access subsystems (`GEditor->GetEditorSubsystem<>()`)
- Create data sources and pass them to Composites via delegates/TAttributes
- Handle the `SWindow` or `SDockTab` lifecycle
- Are the entry point that users or the editor system spawn

## Refactor Mode

For restructuring existing Slate UIs, follow the five-phase process in `refactoring-playbook.md`:

1. **Widget Inventory** — Catalog every widget class, inline tree, and hardcoded style value
2. **Classification and Plan** — Assign each pattern to a level, design canonical widgets
3. **Scaffold Token and Style Layers** — Create tokens and style set alongside existing code
4. **Bottom-Up Extraction** — Extract Primitives → Components → Composites → Layouts → Views
5. **Integration and Cleanup** — Replace inline code, remove old files, verify visually

The key invariant: the project compiles and functions correctly at every intermediate step.

## Composition Rules

These rules apply in both Greenfield and Refactor modes.

1. **One-directional dependency.** Primitives → Components → Composites → Layouts → Views. Never reverse. A Component never imports a Composite. A Primitive never imports a Component.

2. **Primitives and Components are stateless.** They receive all data via `SLATE_ARGUMENT`, `SLATE_ATTRIBUTE`, and `SLATE_EVENT`. No subsystem calls. No global singleton access. No stored data models — only stored TAttributes and delegates.

3. **Composites define data contracts.** Their `SLATE_BEGIN_ARGS` declares domain-specific events (`FOnItemSelected`, `FOnFilterChanged`) and data attributes. The contract is their public API — callers don't know the internal composition.

4. **Layouts are spatial arrangement only.** `SSplitter` ratios, `SDockTab` configurations, `SOverlay` layering. No business logic, no data manipulation, no event handling beyond basic resize and tab management.

5. **Views are the integration point.** They access subsystems, bind delegates, create data sources, and populate Layouts with Composites. All external dependencies enter the widget tree through Views.

6. **No level-skipping.** A Layout should not directly use a Primitive. If it needs a separator between Composites, the Layout uses a Component that wraps that Primitive, or the Composite includes the separator internally.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Widget classes | `S[Prefix][Descriptor]` | `SMyPanel`, `SMyIconButton`, `SMyItemList` |
| Variant enums | `E[Prefix][Type]Variant` | `EMyButtonVariant`, `EMyPanelVariant` |
| Delegates | `FOn[Context][Event]` | `FOnRowCheckboxChanged`, `FOnItemSelected` |
| Token namespaces | `F[Prefix]Spacing`, `F[Prefix]Fonts`, `F[Prefix]Sizing` | `FMySpacing`, `FMyFonts` |
| Color struct | `F[Prefix]Colors` | `FMyColors` |
| Style set | `F[Prefix]SlateStyle` | `FMySlateStyle` |
| Semantic colors | `[Context][Purpose]` members | `BgPanel`, `TextPrimary`, `AccentBlue` |
| Files | PascalCase matching class name | `SMyPanel.h`, `MySlateStyle.cpp` |

**Directory structure:**

```
UI/
├── Tokens/          (MySpacing.h, MyFonts.h, MySizing.h, MyColors.h)
├── Style/           (MySlateStyle.h/.cpp, MyWidgetTypes.h)
└── Widgets/
    ├── Primitives/  (SMyPanel.h/.cpp, SMyIconButton.h/.cpp)
    ├── Components/  (SMyHeaderBar.h/.cpp, SMySearchBar.h/.cpp)
    ├── Composites/  (SMyItemList.h/.cpp, SMyToolbar.h/.cpp)
    ├── Layouts/     (SMyMainLayout.h/.cpp)
    └── Views/       (SMyToolView.h/.cpp)
```

## Quality Checklist

Before considering a Slate UI system complete, verify:

- [ ] Token layer exists — no widget contains hardcoded `FLinearColor`, font size, or spacing value
- [ ] Style set registered — `FSlateStyleSet` subclass with `Initialize()` / `Shutdown()` wired to module lifecycle
- [ ] Every Primitive is stateless — references only tokens and style set, no subsystem access
- [ ] Every Component combines Primitives for a single purpose — describable without "and"
- [ ] Every Composite defines its data contract via `SLATE_EVENT` and `SLATE_ATTRIBUTE`
- [ ] Layouts contain only spatial arrangement — `SSplitter`, `SDockTab`, `SOverlay` with no business logic
- [ ] Views wire everything to real data — subsystem access isolated here
- [ ] Dependency flow is strictly one-directional — no upward imports
- [ ] No duplicate implementations — visual variants use enums, not subclasses
- [ ] All brushes and styles have stable addresses — static or member, never local
- [ ] UIBind reactive pattern used for all color references — live theme updates work
- [ ] `Build.cs` has correct module dependencies — `Slate`, `SlateCore`, and `EditorStyle` if applicable

## Further Reading

- `slate-design-tokens.md` — Complete reference for the token layer: spacing, sizing, font, color, and brush tokens with C++ code examples
- `widget-classification.md` — Decision tree for classifying Slate widgets into the five levels, with worked examples and the Component vs Composite boundary heuristics
- `style-architecture.md` — The `FSlateStyleSet` pattern: central style registry, variant system, live updates, and `FSlateStyleRegistry` integration
- `composition-patterns.md` — `SLATE_BEGIN_ARGS` patterns, delegate communication, `TAttribute` binding, `SOverlay` layering, `SListView` tables, slot patterns, and widget factories
- `refactoring-playbook.md` — Five-phase migration process for restructuring existing Slate UIs with bottom-up extraction and rollback strategy
