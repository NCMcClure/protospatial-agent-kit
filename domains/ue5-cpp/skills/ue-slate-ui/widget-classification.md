# Slate Widget Classification Guide

A systematic framework for classifying Slate widgets into the five-level hierarchy. Use this whenever classification is ambiguous — especially at the Component/Composite boundary, which is the most common source of debate in Slate UI architecture.

## The Five Levels

| Level | What It Is | Slate Construct | Contains | Example |
|-------|-----------|-----------------|----------|---------|
| **Primitive** | Irreducible styled element | `SCompoundWidget` wrapping 1-2 native Slate elements | Only tokens and style set references | Styled panel (SBorder + variant enum), icon button, styled separator |
| **Component** | Small functional group | `SCompoundWidget` composing 2-4 Primitives | Primitives for a single micro-task | Header bar (panel + title + close), labeled field, search bar |
| **Composite** | Recognizable UI section | `SCompoundWidget` with data contract (delegates, TAttributes) | Components, Primitives, other Composites | Filterable list view, toolbar, property panel, tree view |
| **Layout** | Spatial arrangement | SSplitter/SDockTab/SOverlay skeleton | Composite slots, no business logic | Main window skeleton, two-pane editor, tabbed workspace |
| **View** | Layout populated with live data | Top-level widget with subsystem/data access | Populated Layout wired to real data | The actual tool window, settings panel, asset browser |

## The Decision Tree

Work through these five questions in order. The first "yes" determines the level.

### Question 1: Is it an irreducible Slate primitive?

Can this widget be split into smaller meaningful Slate widgets? If splitting it would produce elements with no standalone visual or interactive purpose, it is a **Primitive**.

**Key test:** Does it wrap a single `SBorder`, `STextBlock`, `SButton`, `SImage`, `SCheckBox`, or `SSeparator` — adding design decisions (variant selection, token binding, style set lookup) on top?

**It IS a Primitive if:**
- It wraps one native Slate element with style/token configuration
- Its only dependencies are the token layer and style set
- It has no awareness of what kind of data it displays
- Splitting it further would produce bare Slate elements with no design decisions

**Examples:**
- Styled panel — `SBorder` with variant enum selecting brush from style set
- Icon button — `SButton` with `SImage` + optional `STextBlock`, variant-driven style
- Styled text block — `STextBlock` bound to font token and semantic color
- Styled separator — `SSeparator` with token-driven color and thickness
- Styled checkbox — `SCheckBox` with custom style from style set
- Circular progress indicator — `SLeafWidget` with custom `OnPaint`

**Edge case — SBorder vs styled panel:** A raw `SBorder` with inline `FLinearColor` is not a Primitive. A styled panel that wraps `SBorder` with a variant enum (Light, Dark, Overlay) selecting from the style set IS a Primitive. The distinction is whether *design decisions are encoded and reusable*.

### Question 2: Does it combine a small number of Primitives for one purpose?

If the widget groups 2-4 Primitives that work together for a single micro-task, it is a **Component**.

**The single-sentence test:** Can you describe its purpose in one sentence without the word "and"? If you need "and," it might be a Composite.

**It IS a Component if:**
- It composes 2-4 Primitives
- It serves one purpose describable without "and"
- It has no data contract (no domain-specific SLATE_EVENTs)
- It doesn't contain SListView, STreeView, or other data-bound containers

**Examples:**
- Header bar — panel Primitive + title text Primitive + optional close button Primitive. Purpose: "labels a section with optional dismiss."
- Labeled field — label text Primitive + input widget. Purpose: "presents a labeled input."
- Search bar — text input + search/clear icon button. Purpose: "accepts a search query."
- Toolbar button group — row of icon button Primitives with separator. Purpose: "groups related actions."
- Status indicator — icon Primitive + text Primitive with color binding. Purpose: "shows an item's status."

### Question 3: Does it form a recognizable UI section?

If a non-developer would point at it and name it ("the file list," "the toolbar," "the property panel"), it is a **Composite**.

**Key indicator:** Composites define **data contracts** through `SLATE_EVENT` delegates and `TAttribute` bindings. They declare domain-relevant events like `OnItemSelected`, `OnFilterChanged`, `OnActionTriggered`.

**It IS a Composite if:**
- A stakeholder would name it without prompting
- It declares domain-specific SLATE_EVENTs
- It manages internal state (selection, filtering, expansion)
- It contains SListView, STreeView, or other data-bound containers
- It composes Components and/or Primitives into a functional section

**Examples:**
- Filterable list — SListView + SHeaderRow + search bar Component + OnGenerateRow delegate + selection handling
- Toolbar — multiple button group Components + dropdown menus + context label + state management
- Tree view panel — STreeView + OnGetChildren + expand/collapse + OnSelectionChanged
- Property editor section — SScrollBox of labeled field Components with change delegates
- Tag manager — category tree + item list + search + batch action buttons

### Question 4: Is it a top-level spatial arrangement?

If it defines *where Composites go* — SSplitter ratios, SDockTab slots, SOverlay layers — without containing business logic or real data, it is a **Layout**.

**It IS a Layout if:**
- It uses SSplitter, SDockTab, FTabManager, or SOverlay to arrange regions
- It accepts Composites through named slots or construction parameters
- It contains zero business logic — no subsystem calls, no data manipulation
- It looks like a wireframe in code: boxes and regions, not content

**Examples:**
- Main window skeleton — SSplitter with sidebar region (0.3) + content region (0.7) + optional bottom panel
- Two-pane editor — left list panel + right detail panel with SSplitter
- Tabbed workspace — SDockTab registration + FTabManager configuration + tab spawner callbacks
- Overlay layout — SOverlay with content layer + notification layer + modal layer

### Question 5: Is it a Layout populated with live data?

If it instantiates a Layout and wires it to subsystems, delegates, settings, and real data sources, it is a **View**.

**It IS a View if:**
- It creates a Layout and populates it with Composites
- It accesses subsystems (`GEditor->GetEditorSubsystem<>()`)
- It binds real data sources to Composite delegates and TAttributes
- It handles the SWindow lifecycle (creation, title, sizing)
- It is the entry point that users or the editor system spawn

**Examples:**
- The actual tool window that creates the main window Layout, retrieves data from a subsystem, and passes it to list/tree Composites
- The settings view that populates a property editor Layout with UDeveloperSettings values
- The asset browser view that wires an asset registry query to a filterable list Composite

## The Component vs Composite Boundary

This is the most common classification debate in Slate. Five heuristics to resolve it:

### Heuristic 1: Stakeholder Naming

Would a designer or PM point at it and give it a name unprompted? "The file browser" = Composite. "The search bar" = Component. If a non-developer would call it "that search thingy at the top," it's a Component. If they'd call it "the file browser" or "the settings panel," it's a Composite.

### Heuristic 2: Single Responsibility

Describe what it does without "and":
- Search bar: "accepts a search query" → **Component**
- Filterable list: "shows items AND filters them AND allows selection AND generates rows" → **Composite**
- Header bar: "labels a section with optional dismiss" → **Component**
- Toolbar: "provides actions AND shows context AND manages state" → **Composite**

### Heuristic 3: Data Contract Complexity

Does it declare `SLATE_EVENT` delegates for meaningful domain events?
- `FSimpleDelegate OnClicked` or `FOnTextChanged OnSearchChanged` → simple pass-through, **Component**
- `FOnItemSelected`, `FOnFilterChanged`, `FOnBatchOperationComplete` → domain-specific contract, **Composite**

The distinction is whether the events describe domain concepts (item selection, filter changes) or generic UI interactions (click, text change).

### Heuristic 4: SListView/STreeView Presence

Any widget containing `SListView` or `STreeView` with `OnGenerateRow`/`OnGetChildren` is almost always a **Composite**. These containers inherently manage data (items source, row generation, selection state) and define non-trivial data contracts. Even a "simple" SListView needs row generation logic, which puts it beyond Component scope.

### Heuristic 5: When in Doubt, Go Higher

If a widget sits on the boundary, classify it as **Composite**. It's cheaper to demote a Composite to a Component later (remove delegates, simplify) than to promote a Component to a Composite (add delegates, extract state management, refactor callers).

## Worked Examples

### Example 1: Styled SBorder with Variant Enum

A widget that wraps `SBorder`, accepts a variant enum (Light, Dark, Overlay), selects a brush from the style set, and accepts a content slot.

**Classification: Primitive.** It wraps a single native element with style decisions encoded. Even with three variants, it remains irreducible — each variant is just a different brush selection, not a different composition.

### Example 2: Header Bar with Title and Close Button

A widget composing a panel Primitive + title text block + optional close icon button. Has `SLATE_ATTRIBUTE(FText, Title)` and `SLATE_EVENT(FSimpleDelegate, OnCloseClicked)`.

**Classification: Component.** Three Primitives, one purpose. "Labels a section with optional dismiss" — one sentence, no "and." The `OnCloseClicked` delegate is generic UI interaction, not a domain event.

### Example 3: SListView-Based Tagged Item List

A widget with `SListView<TSharedPtr<FMyItem>>`, `SHeaderRow` with multiple columns, search/filter bar Component, `OnGenerateRow` callback, selection handling, and `SLATE_EVENT(FOnItemSelected, OnItemSelected)`.

**Classification: Composite.** Heuristic 4 (SListView presence) alone is decisive. It also passes all other tests: a stakeholder would name it ("the items list"), it has a domain-specific data contract, and describing it requires "and."

### Example 4: Toolbar — When Complexity Matters

**Scenario A:** A horizontal row of 3 icon button Primitives with a separator between them.
**Classification: Component.** "Groups related actions" — single purpose, simple composition.

**Scenario B:** A toolbar with multiple button groups, a dropdown menu, a context label showing selection count, undo/redo state, and `SLATE_EVENT(FOnActionTriggered, OnAction)`.
**Classification: Composite.** Multiple concerns, domain-specific events, internal state management. Apply Heuristic 2 — you need "and" to describe it.

### Example 5: SOverlay Hover Effects on a List Row

A list row widget using `SOverlay` to layer: background (layer 0) + content columns (layer 1) + hover action buttons (layer 2, visibility-bound to hover state).

**Classification: Component.** The row widget is used inside a Composite's `OnGenerateRow` callback. It composes Primitives (text blocks, icon buttons, progress indicator) for a single purpose: "displays one item's data with hover actions." The `SOverlay` is an implementation detail enabling the hover pattern, not a classification level. The row is a Component; the containing list is the Composite.

### Example 6: Main Window with SSplitter

**Scenario A:** A widget that uses `SSplitter` to arrange a sidebar and content area, accepting Composites through named slots, with zero business logic.
**Classification: Layout.** Pure spatial arrangement.

**Scenario B:** Same structure but also creates subsystem references, manages tab state, handles window lifecycle, and wires data to child Composites.
**Classification: View.** It has crossed from arrangement into integration.

**Scenario C:** Same structure but contains some section logic (managing an overlay's visibility) alongside the SSplitter arrangement.
**Classification: Composite that should be decomposed.** Extract the spatial arrangement into a Layout, extract the overlay logic into a Composite, and create a View that wires them together.

## Common Misclassifications

**Wrapping every SBorder in a Primitive.** Not every `SBorder` needs its own widget class. Only create a Primitive when the `SBorder` encodes a *reusable design decision* — a variant enum selecting from the style set, token-bound colors, a specific border + background combination used in multiple places. A one-off `SBorder` with padding inside a Composite's `Construct` is fine as inline code.

**SListView inside a Component.** If you've put `SListView` with `OnGenerateRow` inside what you're calling a Component, it has outgrown that level. Promote to Composite. `SListView` inherently manages data (items source, row lifecycle, selection) which requires a non-trivial data contract.

**Subsystem access in Composites.** Composites define data contracts via delegates and `TAttribute` — they declare *what data they need*, not *where it comes from*. If a Composite calls `GEditor->GetEditorSubsystem<>()` or accesses a global singleton, that access belongs in the View. Pass the data down through the contract.

**Confusing Layouts with Composites.** A Layout is not a big Composite. It is *spatial arrangement only* — SSplitter ratios, SDockTab slots, SOverlay layers. No business logic, no data manipulation, no event handling beyond basic resize/tab management. If it processes data or fires domain events, it's a Composite (or a Composite + Layout that should be separated).

**Classifying utility widgets.** Infrastructure widgets like `SBox` wrappers, `SScrollBox` containers, custom `SSplitter` configurations, and `SWidgetSwitcher` setups are not classified in the five levels. They are plumbing that supports the hierarchy. Place them in a separate `Utils/` directory if you extract them as reusable helpers.

**Creating Primitives for Slate built-ins.** Don't create an `SMyTextBlock` Primitive that just wraps `STextBlock` with `.Font(FMyFonts::Regular())`. That's not a design decision — it's a convenience wrapper that adds indirection without value. A Primitive earns its existence by encoding a *non-trivial* design decision: variant selection, multi-element composition (icon + text), custom paint behavior, or reactive token binding that would otherwise be repeated across many call sites.
