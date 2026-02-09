# Refactoring Playbook: Migrating Existing Slate UIs

A phase-based process for restructuring existing Slate widget hierarchies into the five-level system (Primitives → Components → Composites → Layouts → Views) without changing visual or functional behavior.

## Before You Start

**Prerequisites:**
- The existing Slate UI compiles and runs correctly
- You can visually verify the UI (open the tool, see every panel and state)
- You've agreed on project prefix, token naming, and directory structure conventions
- You've identified a **pilot scope** — one panel or window, not the entire UI

**Do not** refactor everything at once. Pick the most self-contained window or panel. Get it through all five phases. Learn what works. Then expand to the next section.

**Invariant:** The project must compile and function correctly at every intermediate step. If it doesn't, you've taken too large a step. Back up and decompose further.

## Phase 1: Widget Inventory

The goal of Phase 1 is to catalog what exists — every widget class, every inline widget tree, every hardcoded style value.

### Step 1.1: Crawl Existing SWidget Subclasses

Find every class inheriting from `SCompoundWidget`, `SLeafWidget`, or other `SWidget` bases in your pilot scope.

Search patterns:
- `class S*` in headers under your UI directories
- `SCompoundWidget` / `SLeafWidget` / `SMultiColumnTableRow` base classes
- `SLATE_BEGIN_ARGS` declarations

Record each widget:

| Widget Class | File | Base Class | Lines in Construct | Creates Inline? | Description |
|-------------|------|-----------|-------------------|----------------|-------------|
| `SMyMainWindow` | MainWindow.h | SCompoundWidget | 280 | Yes (heavy) | Top-level tool window |
| `SMySettingsPanel` | SettingsPanel.h | SCompoundWidget | 45 | Minimal | Settings section |
| `SMyItemList` | ItemList.h | SCompoundWidget | 150 | Moderate | List view with rows |

### Step 1.2: Identify Inline Widget Creation

The biggest refactoring opportunity. Look for `Construct` methods that build large widget trees with deeply nested `SNew` calls instead of composing named widget classes.

**What a monolith looks like:**

```cpp
void SMyMainWindow::Construct(const FArguments& InArgs)
{
    ChildSlot
    [
        SNew(SVerticalBox)
        + SVerticalBox::Slot().AutoHeight()
        [
            SNew(SBorder)                          // ← implicit header panel
            .BorderImage(/* hardcoded brush */)
            .Padding(8.0f)
            [
                SNew(SHorizontalBox)
                + SHorizontalBox::Slot().FillWidth(1.0f)
                [
                    SNew(STextBlock)               // ← implicit title text
                    .Text(LOCTEXT("Title", "My Tool"))
                    .Font(FCoreStyle::GetDefaultFontStyle("Bold", 14))
                ]
                + SHorizontalBox::Slot().AutoWidth()
                [
                    SNew(SButton)                  // ← implicit close button
                    .OnClicked(/* ... */)
                    [SNew(SImage).Image(/* X icon */)]
                ]
            ]
        ]
        + SVerticalBox::Slot().FillHeight(1.0f)
        [
            // ... 200 more lines of inline SNew calls
        ]
    ];
}
```

This `Construct` contains implicit Primitives (styled border, icon button), implicit Components (header bar), and possibly implicit Composites (list sections, toolbars) — all inlined.

**Catalog each inline section:**

| Inline Section | Location | What It Contains | Target Level |
|---------------|----------|-----------------|-------------|
| Header panel (L12-30) | MainWindow.cpp | Border + title + close button | Component |
| Search bar (L32-45) | MainWindow.cpp | Text input + icon button | Component |
| Item list (L48-180) | MainWindow.cpp | SListView + header row + rows | Composite |
| Status footer (L182-200) | MainWindow.cpp | Text + progress bar | Component |

### Step 1.3: Catalog Visual Patterns

Group by visual function across all widgets in scope. This reveals duplication — the same panel border in five places, the same button style in twelve places.

| Pattern | Occurrences | Variations | Files |
|---------|------------|------------|-------|
| Panel background border | 8 | 3 (light, dark, semi-transparent) | MainWindow, SettingsPanel, ItemList |
| Icon buttons | 12 | 4 styles (solid, transparent, invisible, toggle) | Throughout |
| Section headers | 4 | 2 (with close, without close) | MainWindow, SettingsPanel |
| List rows | 1 template | Hover actions overlay | ItemList |

### Step 1.4: Catalog Hardcoded Style Values

Grep for hardcoded visual values that should become tokens.

**Search patterns:**

```
FLinearColor(           → color tokens
FColor(                 → color tokens
FMargin(N.Nf            → spacing tokens (where N is a literal number)
.Padding(N.Nf           → spacing tokens
GetDefaultFontStyle("   → font tokens
FVector2D(N.Nf, N.Nf)   → sizing tokens (for icon sizes)
.FixedWidth(N.Nf)       → sizing tokens
.HeightOverride(N.Nf)   → sizing tokens
```

Record each unique value and its count:

| Hardcoded Value | Count | Proposed Token |
|----------------|-------|---------------|
| `FMargin(8.0f)` | 14 | `FMySpacing::MD` |
| `FMargin(4.0f)` | 9 | `FMySpacing::XS` |
| `FLinearColor(0.15f, 0.15f, 0.15f, 1.0f)` | 6 | `FMyColors::BgPanel` |
| `GetDefaultFontStyle("Bold", 14)` | 3 | `FMyFonts::Heading()` |
| `FVector2D(16.0f, 16.0f)` | 8 | `FMySizing::IconMD` |

## Phase 2: Classification and Plan

### Step 2.1: Classify Every Pattern

Using the decision tree in `widget-classification.md`, assign each cataloged pattern (from 1.3) and each inline section (from 1.2) to a level.

| Pattern/Section | Level | Canonical Widget Name | Replaces |
|----------------|-------|----------------------|----------|
| Panel background | Primitive | `SMyPanel` | 8 inline SBorder instances |
| Icon button | Primitive | `SMyIconButton` | 12 inline SButton+SImage |
| Section header | Component | `SMyHeaderBar` | 4 inline header blocks |
| Search bar | Component | `SMySearchBar` | 2 inline search blocks |
| Item list | Composite | `SMyItemList` | 1 monolith section |
| Main window arrangement | Layout | `SMyMainLayout` | Inline SSplitter in MainWindow |
| Tool window | View | `SMyToolView` | SMyMainWindow (refactored) |

### Step 2.2: Design Canonical Widgets

For each group of related patterns, design a single widget class with variant enum or configuration props.

**Example — SMyPanel canonical design:**

```
SMyPanel
├── SLATE_ARGUMENT: EMyPanelVariant Variant (Light, Dark, Overlay)
├── SLATE_ATTRIBUTE: —
├── SLATE_EVENT: —
├── SLATE_DEFAULT_SLOT: Content
├── Replaces: 8 inline SBorder with 3 different color schemes
└── References: FMySlateStyle::GetPanelBrush(Variant)
```

**Example — SMyIconButton canonical design:**

```
SMyIconButton
├── SLATE_ARGUMENT: EMyButtonVariant Variant (Standard, Simple, NoBorder)
├── SLATE_ARGUMENT: const FSlateBrush* IconBrush
├── SLATE_ATTRIBUTE: FText Text (optional)
├── SLATE_ATTRIBUTE: FVector2D IconSize
├── SLATE_EVENT: FOnClicked OnClicked
├── Replaces: 12 inline SButton+SImage combos
└── References: FMySlateStyle::GetButtonStyle(Variant)
```

### Step 2.3: Map Dependencies

Verify one-directional flow in your classification:

```
Primitives: SMyPanel, SMyIconButton, SMyStyledText
    ↓ (used by)
Components: SMyHeaderBar, SMySearchBar, SMyStatusBar
    ↓ (used by)
Composites: SMyItemList, SMyToolbar, SMySettingsSection
    ↓ (used by)
Layouts: SMyMainLayout
    ↓ (used by)
Views: SMyToolView
```

**Common issue:** An existing widget classified as a Component directly calls `GEditor->GetEditorSubsystem<>()`. This subsystem access must move to the View level. The Component declares a `SLATE_EVENT` or `SLATE_ATTRIBUTE` instead, and the View provides the data.

## Phase 3: Scaffold Token and Style Layers

### Step 3.1: Create Token Files

Build the token namespaces/structs from the hardcoded values found in Phase 1 (Step 1.4). Do not update existing widgets yet — just create the definitions.

Create these files (see `slate-design-tokens.md` for complete format):
- `MySpacing.h` — FMySpacing namespace
- `MySizing.h` — FMySizing namespace
- `MyFonts.h` — FMyFonts namespace
- `MyColors.h` — FMyColors struct + UIBind functions

### Step 3.2: Create the Style Set

Build the `FSlateStyleSet` subclass with all brush and style variants identified in Phase 2 (see `style-architecture.md` for complete pattern).

- Register with `FSlateStyleRegistry` in module startup
- Wire settings change delegate to `UpdateStyles()`
- Define static style members for each variant

### Step 3.3: Create Parallel Directory Structure

Create the target structure alongside existing code. Do not move or modify existing files.

```
Source/MyModule/
├── UI/                     ← existing (untouched)
│   ├── SMyMainWindow.h
│   ├── SMyMainWindow.cpp
│   ├── SMyItemList.h
│   └── SMyItemList.cpp
└── SlateUI/                ← new (target structure)
    ├── Tokens/
    │   ├── MySpacing.h
    │   ├── MySizing.h
    │   ├── MyFonts.h
    │   └── MyColors.h
    ├── Style/
    │   ├── MySlateStyle.h
    │   ├── MySlateStyle.cpp
    │   └── MyWidgetTypes.h     ← variant enums
    └── Widgets/
        ├── Primitives/
        ├── Components/
        ├── Composites/
        ├── Layouts/
        └── Views/
```

**Verify:** The project compiles. The new files exist alongside the old code. Nothing has changed functionally.

## Phase 4: Bottom-Up Extraction

Extract widgets from the bottom of the hierarchy upward. Each extraction step should leave the project compiling and functioning.

### Step 4.1: Extract Primitives

Start with the most-reused elements. Each Primitive is a standalone `SCompoundWidget` in the `Primitives/` directory.

**Before** (inline in a monolith):
```cpp
// In SMyMainWindow::Construct, line 12
SNew(SBorder)
.BorderImage(FAppStyle::GetBrush(TEXT("WhiteBrush")))
.BorderBackgroundColor(FLinearColor(0.15f, 0.15f, 0.15f, 1.0f))
.Padding(8.0f)
[Content]
```

**After** (extracted Primitive):
```cpp
// SMyPanel.h — standalone Primitive
class SMyPanel : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SMyPanel)
        : _Variant(EMyPanelVariant::Light)
        , _Padding(FMySpacing::MD)
    {}
        SLATE_ARGUMENT(EMyPanelVariant, Variant)
        SLATE_ARGUMENT(FMargin, Padding)
        SLATE_DEFAULT_SLOT(FArguments, Content)
    SLATE_END_ARGS()

    void Construct(const FArguments& InArgs);
};

// Usage (replacing the inline SBorder):
SNew(SMyPanel)
.Variant(EMyPanelVariant::Light)
[Content]
```

**Verify** each Primitive: Construct it inline in the existing code. Visual output must be identical.

### Step 4.2: Extract Components

Components compose the newly created Primitives.

**Before** (inline header in a monolith):
```cpp
SNew(SBorder).BorderImage(/*...*/).Padding(8.0f)
[
    SNew(SHorizontalBox)
    + SHorizontalBox::Slot().FillWidth(1.0f).VAlign(VAlign_Center)
    [SNew(STextBlock).Text(Title).Font(/*hardcoded*/)]
    + SHorizontalBox::Slot().AutoWidth()
    [SNew(SButton).OnClicked(OnClose)[SNew(SImage).Image(XIcon)]]
]
```

**After** (extracted Component using Primitives):
```cpp
SNew(SMyHeaderBar)
.Title(LOCTEXT("ToolTitle", "My Tool"))
.bShowCloseButton(true)
.OnCloseClicked(this, &SMyMainWindow::HandleClose)
```

### Step 4.3: Extract Composites

This is the largest change. Existing monolithic widgets often have list views, toolbars, and property panels inline.

**Key actions:**
- Extract each recognizable section into its own Composite
- The Composite's `SLATE_EVENT` declarations form its data contract
- Remove subsystem access from the Composite — push it up to View level
- Wire delegates from Composite events to parent handlers

**Before** (inline list in a monolith, ~130 lines):
```cpp
// SListView creation, OnGenerateRow, header row, filtering logic
// all inline in SMyMainWindow::Construct
```

**After** (extracted Composite):
```cpp
SNew(SMyItemList)
.ItemsSource(&Items)
.OnItemSelected(this, &SMyToolView::HandleItemSelected)
.OnItemDeleted(this, &SMyToolView::HandleItemDeleted)
```

### Step 4.4: Extract Layouts

Create spatial arrangement skeletons that accept Composites through named slots.

```cpp
// SMyMainLayout — pure spatial arrangement
class SMyMainLayout : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SMyMainLayout) {}
        SLATE_NAMED_SLOT(FArguments, Sidebar)
        SLATE_NAMED_SLOT(FArguments, Content)
        SLATE_NAMED_SLOT(FArguments, Footer)
    SLATE_END_ARGS()

    void Construct(const FArguments& InArgs)
    {
        ChildSlot
        [
            SNew(SVerticalBox)
            + SVerticalBox::Slot().FillHeight(1.0f)
            [
                SNew(SSplitter).Orientation(Orient_Horizontal)
                + SSplitter::Slot().Value(0.3f)[InArgs._Sidebar.Widget]
                + SSplitter::Slot().Value(0.7f)[InArgs._Content.Widget]
            ]
            + SVerticalBox::Slot().AutoHeight()
            [InArgs._Footer.Widget]
        ];
    }
};
```

### Step 4.5: Wire Views

Create the View-level widget that populates the Layout with Composites and real data.

```cpp
void SMyToolView::Construct(const FArguments& InArgs)
{
    // View accesses subsystems and data sources
    MySubsystem = GEditor->GetEditorSubsystem<UMyEditorSubsystem>();
    Items = MySubsystem->GetItems();

    ChildSlot
    [
        SNew(SMyMainLayout)
        .Sidebar()
        [
            SNew(SMyItemList)
            .ItemsSource(&Items)
            .OnItemSelected(this, &SMyToolView::HandleItemSelected)
        ]
        .Content()
        [
            SNew(SMyDetailPanel)
            .Item(this, &SMyToolView::GetSelectedItem)
        ]
        .Footer()
        [
            SNew(SMyStatusBar)
            .ItemCount(this, &SMyToolView::GetItemCount)
        ]
    ];
}
```

## Phase 5: Integration and Cleanup

### Step 5.1: Replace Inline Code

Go through the original monolithic widgets and replace inline construction with calls to the new extracted widgets. This can be done incrementally — one extraction at a time.

After all replacements, the original monolithic `Construct` method should be short — it either delegates entirely to a View or has been replaced by the View.

### Step 5.2: Remove Old Code

Once the monolithic `Construct` methods are fully decomposed:
- If the old widget class is now just a thin wrapper around the View, remove it and use the View directly
- If tab spawners or external references point to the old class, update them
- Delete unused source files

### Step 5.3: Update Build.cs

Verify module dependencies. The new token/style files typically don't need new dependencies, but verify:
- `Slate` and `SlateCore` are listed (they usually already are)
- `EditorStyle` or `EditorFramework` is listed if using `FAppStyle`
- `InputCore` is listed if handling input events
- No circular dependencies were introduced

### Step 5.4: Visual Verification

Open every panel and window. Compare against pre-refactor state. Every pixel should match.

If something looks different:
1. Check the token value — does `FMySpacing::MD` match the original `8.0f`?
2. Check the brush — does the style set produce the same color and corner radius?
3. Check the color binding — is `UIBind(&FMyColors::BgPanel)` returning the same linear color?
4. Trace to the token/style layer. Never patch at the View level — fix the foundation.

## Introducing Tokens into Existing Code

A focused technique for the token migration specifically. This can be done as a standalone step without the full five-phase refactoring.

### Search-and-Replace Strategy

Do one token type at a time across the entire pilot scope:

**Pass 1 — Spacing:**
```
Find:    .Padding(8.0f)
Replace: .Padding(FMySpacing::MD)

Find:    FMargin(4.0f)
Replace: FMargin(FMySpacing::XS)

Find:    .Padding(4.0f, 0.0f)
Replace: .Padding(FMySpacing::XS, 0.0f)
```

**Pass 2 — Fonts:**
```
Find:    FCoreStyle::GetDefaultFontStyle("Regular", 10)
Replace: FMyFonts::Regular()

Find:    FCoreStyle::GetDefaultFontStyle("Bold", 14)
Replace: FMyFonts::Heading()
```

**Pass 3 — Sizing:**
```
Find:    FVector2D(16.0f, 16.0f)  (when used for icon sizing)
Replace: FVector2D(FMySizing::IconMD, FMySizing::IconMD)

Find:    .FixedWidth(120.0f)
Replace: .FixedWidth(FMySizing::ColumnStatusWidth)
```

**Pass 4 — Colors (the UIBind migration):**
```
Find:    .ColorAndOpacity(FSlateColor(FLinearColor(0.86f, 0.86f, 0.86f, 1.0f)))
Replace: .ColorAndOpacity(UIBind(&FMyColors::TextPrimary))

Find:    .BorderBackgroundColor(FLinearColor(0.2f, 0.2f, 0.2f, 1.0f))
Replace: .BorderBackgroundColor(UIBind(&FMyColors::BgPanel))
```

After each pass, compile and visually verify. The UI should look identical.

## Testing Strategies

### Visual Verification

Slate does not have built-in visual regression testing. The pragmatic approach:

**Manual comparison:** Take screenshots before refactoring. After each extraction, compare against the reference. Check every state: default, hovered, selected, disabled, empty data, many items, long text.

**Isolation testing:** Spawn individual Primitives and Components in a test `SWindow` to verify they render correctly in isolation:

```cpp
// In a debug/test function:
TSharedRef<SWindow> TestWindow = SNew(SWindow)
    .Title(LOCTEXT("Test", "Widget Test"))
    .ClientSize(FVector2D(400, 300))
    [
        SNew(SVerticalBox)
        + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
        [SNew(SMyPanel).Variant(EMyPanelVariant::Light)[SNew(STextBlock).Text(LOCTEXT("Light", "Light"))]]
        + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
        [SNew(SMyPanel).Variant(EMyPanelVariant::Dark)[SNew(STextBlock).Text(LOCTEXT("Dark", "Dark"))]]
        + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
        [SNew(SMyPanel).Variant(EMyPanelVariant::Overlay)[SNew(STextBlock).Text(LOCTEXT("Overlay", "Overlay"))]]
    ];
FSlateApplication::Get().AddWindow(TestWindow);
```

### Functional Verification

Test the data flow with UE5's automation framework:

**Delegate flow:** Fire an event on a Composite, verify the handler is called in the View.

**TAttribute binding:** Change a bound value, verify the widget reads the new value on the next `Tick`.

**Variant correctness:** Construct a widget with each variant, verify the correct style is applied by checking the brush pointer matches the expected static member.

```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FMyPanelVariantTest,
    "MyProject.SlateUI.Panel.Variants",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FMyPanelVariantTest::RunTest(const FString& Parameters)
{
    // Verify each variant maps to the correct brush
    const FSlateBrush& LightBrush = FMySlateStyle::GetPanelBrush(EMyPanelVariant::Light);
    const FSlateBrush& DarkBrush = FMySlateStyle::GetPanelBrush(EMyPanelVariant::Dark);

    TestTrue("Light and Dark brushes are different", &LightBrush != &DarkBrush);
    return true;
}
```

## Rollback Strategy

The refactoring is designed so that you can stop and roll back at any phase boundary.

**Phase 3 rollback** (scaffolding): Delete the new `SlateUI/` directory. Zero impact — old code is untouched.

**Phase 4 rollback** (extraction): New widgets exist alongside old code. Delete new widget files. Old monolithic widgets still compile and function because they were never modified (extractions were created in parallel, not by editing the originals).

**Phase 5 rollback** (integration): If replacing inline code with extracted widget calls causes issues, revert the replacement. The inline code is in version control. The extracted widgets remain available for a second attempt.

**The key invariant:** At no point during Phases 3-4 is old code deleted or modified. Old and new code coexist. Only in Phase 5 do you modify the original code by replacing inline sections with calls to extracted widgets. And only after full visual verification do you delete the old inline code.
