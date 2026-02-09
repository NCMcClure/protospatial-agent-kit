# Slate Composition Patterns

Slate's declarative C++ syntax provides a rich set of composition tools. This reference covers the patterns used to build widgets at every level of the hierarchy — from Primitive construction arguments to Layout-level spatial arrangement.

## SLATE_BEGIN_ARGS Patterns

Every custom Slate widget declares its construction interface through the `SLATE_BEGIN_ARGS` / `SLATE_END_ARGS` block. Four macro types define different categories of construction parameters.

### The Four Argument Types

```cpp
class SMyWidget : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SMyWidget)
        : _Variant(EMyWidgetVariant::Standard)  // default value
        , _bShowCloseButton(false)
    {}
        // --- SLATE_ARGUMENT: static config, set once at construction ---
        SLATE_ARGUMENT(EMyWidgetVariant, Variant)
        SLATE_ARGUMENT(bool, bShowCloseButton)
        SLATE_ARGUMENT(const FSlateBrush*, IconBrush)

        // --- SLATE_ATTRIBUTE: dynamic values, can change every frame ---
        SLATE_ATTRIBUTE(FText, Title)
        SLATE_ATTRIBUTE(EVisibility, CloseButtonVisibility)
        SLATE_ATTRIBUTE(FSlateColor, TextColor)

        // --- SLATE_EVENT: delegate callbacks to parent ---
        SLATE_EVENT(FSimpleDelegate, OnCloseClicked)
        SLATE_EVENT(FOnTextChanged, OnSearchChanged)

        // --- SLATE_DEFAULT_SLOT / SLATE_NAMED_SLOT: child content ---
        SLATE_DEFAULT_SLOT(FArguments, Content)
        SLATE_NAMED_SLOT(FArguments, HeaderContent)
        SLATE_NAMED_SLOT(FArguments, FooterContent)
    SLATE_END_ARGS()

    void Construct(const FArguments& InArgs);
};
```

**When to use each:**

| Macro | Stored As | Changes At Runtime? | Use For |
|-------|-----------|-------------------|---------|
| `SLATE_ARGUMENT` | Plain value (`T`) | No | Variant enums, booleans, brush pointers, static config |
| `SLATE_ATTRIBUTE` | `TAttribute<T>` | Yes (polled every frame) | Text, visibility, colors, enabled state — anything dynamic |
| `SLATE_EVENT` | Delegate (`FOnClicked`, etc.) | N/A | Callbacks to parent: clicks, selections, value changes |
| `SLATE_DEFAULT_SLOT` | `TAlwaysValidWidget` | No (set at construction) | Single child content: `SNew(SMyWidget)[ child ]` |
| `SLATE_NAMED_SLOT` | `TAlwaysValidWidget` | No (set at construction) | Multiple named injection points |

### Construct Implementation

```cpp
void SMyWidget::Construct(const FArguments& InArgs)
{
    // Store what you need beyond Construct
    Variant = InArgs._Variant;             // ARGUMENT: direct value
    Title = InArgs._Title;                  // ATTRIBUTE: stored as TAttribute<FText>
    OnCloseClicked = InArgs._OnCloseClicked; // EVENT: stored as delegate

    // Select style based on variant
    const FSlateBrush& PanelBrush = FMySlateStyle::GetPanelBrush(
        InArgs._Variant == EMyWidgetVariant::Standard
            ? EMyPanelVariant::Light
            : EMyPanelVariant::Dark);

    // Build the widget tree
    ChildSlot
    [
        SNew(SBorder)
        .BorderImage(&PanelBrush)
        .Padding(FMySpacing::MD)
        [
            SNew(SVerticalBox)

            // Header with close button
            + SVerticalBox::Slot()
            .AutoHeight()
            [
                SNew(SHorizontalBox)
                + SHorizontalBox::Slot()
                .FillWidth(1.0f)
                .VAlign(VAlign_Center)
                [
                    SNew(STextBlock)
                    .Text(InArgs._Title)  // TAttribute — bound dynamically
                    .Font(FMyFonts::LargeBold())
                    .ColorAndOpacity(UIBind(&FMyColors::TextPrimary))
                ]
                + SHorizontalBox::Slot()
                .AutoWidth()
                [
                    SNew(SMyIconButton)
                    .Variant(EMyButtonVariant::NoBorder)
                    .IconBrush(FAppStyle::GetBrush(TEXT("Icons.X")))
                    .OnClicked(InArgs._OnCloseClicked)
                    .Visibility(InArgs._CloseButtonVisibility)
                ]
            ]

            // Content area — accepts child via default slot
            + SVerticalBox::Slot()
            .FillHeight(1.0f)
            [
                InArgs._Content.Widget
            ]
        ]
    ];
}
```

**Naming convention:** The SLATE macros generate members with underscore prefix (`_Variant`, `_Title`) in the `FArguments` struct. In your widget's member variables, store without the prefix. The Slate `SNew` syntax strips the underscore: `.Variant(value)`, `.Title(text)`.

## Delegate Patterns

Delegates are the communication channel between widgets. Children fire events upward; parents never reach down into children. This enforces the one-directional dependency flow.

### Pattern 1: Simple Notification (No Payload)

```cpp
// The widget fires it; the parent handles it
SLATE_EVENT(FSimpleDelegate, OnCloseClicked)

// Parent binds:
SNew(SMyHeaderBar)
.OnCloseClicked(FSimpleDelegate::CreateSP(this, &SMyParent::HandleClose))

// Or with shorthand:
.OnCloseClicked(this, &SMyParent::HandleClose)
```

### Pattern 2: Single Value Payload

```cpp
// Declare a custom delegate type
DECLARE_DELEGATE_OneParam(FOnItemSelected, TSharedPtr<FMyItem> /*SelectedItem*/);

// In SLATE_BEGIN_ARGS:
SLATE_EVENT(FOnItemSelected, OnItemSelected)

// Child fires:
OnItemSelected.ExecuteIfBound(SelectedItem);

// Parent binds:
SNew(SMyListView)
.OnItemSelected(this, &SMyParent::HandleItemSelected)
```

### Pattern 3: Multi-Value Payload

```cpp
DECLARE_DELEGATE_TwoParams(FOnRowAction, TSharedPtr<FMyItem> /*Item*/, EMyAction /*Action*/);
SLATE_EVENT(FOnRowAction, OnRowAction)

// Child fires:
OnRowAction.ExecuteIfBound(Item, EMyAction::Delete);
```

### Pattern 4: Return Value Delegate

Used when the parent needs to provide computed data back to the child.

```cpp
DECLARE_DELEGATE_RetVal_OneParam(FText, FOnGetItemTooltip, TSharedPtr<FMyItem> /*Item*/);
SLATE_EVENT(FOnGetItemTooltip, OnGetItemTooltip)

// Child queries:
FText Tooltip = OnGetItemTooltip.IsBound()
    ? OnGetItemTooltip.Execute(Item)
    : FText::GetEmpty();

// Parent provides:
SNew(SMyListRow)
.OnGetItemTooltip(this, &SMyComposite::GetTooltipForItem)
```

### Delegate Naming Convention

| Pattern | Name Format | Example |
|---------|------------|---------|
| Action occurred | `FOn[Context][Action]` | `FOnRowCheckboxChanged`, `FOnItemDoubleClicked` |
| Request data | `FOnGet[Thing]` | `FOnGetItemTooltip`, `FOnGetRowColor` |
| Lifecycle | `FOn[Widget][Event]` | `FOnListRefreshed`, `FOnPanelClosed` |

## TAttribute Binding

`TAttribute<T>` is Slate's reactive mechanism. Any property declared as `SLATE_ATTRIBUTE` can be bound to a value that changes every frame. Slate polls the bound lambda/delegate during its paint pass.

### Three Binding Modes

**Static value** — fixed at construction, never changes:

```cpp
SNew(STextBlock)
.Text(FText::FromString(TEXT("Hello")))
```

**Lambda binding** — recomputed every frame:

```cpp
SNew(STextBlock)
.Text_Lambda([this]()
{
    return FText::Format(LOCTEXT("CountFmt", "{0} items selected"), SelectedCount);
})
```

**Member function binding** — calls a method on an object every frame:

```cpp
SNew(STextBlock)
.Text(this, &SMyWidget::GetStatusText)

// Where:
FText SMyWidget::GetStatusText() const
{
    return FText::FromString(CurrentStatus);
}
```

### Visibility Binding

The most common TAttribute pattern — controlling widget visibility:

```cpp
SNew(SMyActionButtons)
.Visibility_Lambda([this]()
{
    return bIsHovered ? EVisibility::Visible : EVisibility::Collapsed;
})
```

**Visibility values:**
- `EVisibility::Visible` — renders and accepts input
- `EVisibility::Collapsed` — hidden, takes no space, no input
- `EVisibility::Hidden` — hidden but reserves space, no input
- `EVisibility::HitTestInvisible` — visible but ignores input (passes through to layers below)
- `EVisibility::SelfHitTestInvisible` — visible, self ignores input but children can receive it

### Lifecycle Considerations

**Capturing `this` in lambdas:** If the widget that owns the lambda is destroyed while the child widget (and its TAttribute) still exists, the lambda captures a dangling pointer. Guard with `TWeakPtr`:

```cpp
TWeakPtr<SMyWidget> WeakSelf = SharedThis(this);
SNew(STextBlock)
.Text_Lambda([WeakSelf]()
{
    if (TSharedPtr<SMyWidget> Self = WeakSelf.Pin())
    {
        return Self->GetStatusText();
    }
    return FText::GetEmpty();
})
```

In practice, this is rarely needed because Slate widget trees are destroyed top-down — parents before children. But if you pass TAttribute-bound widgets to external owners (SDockTab, SWindow), guard the binding.

**Performance:** TAttribute lambdas are called every frame. Keep them fast — member access and simple computation only. Never trigger allocations, async operations, or subsystem queries inside a TAttribute lambda.

## SOverlay Layering

`SOverlay` composites multiple widgets in the same space, rendering back-to-front. The most useful pattern is the hover-action overlay on list rows.

### Background + Content + Hover Actions

```cpp
ChildSlot
[
    SNew(SOverlay)

    // Layer 0: Background (colored on hover/selection)
    + SOverlay::Slot()
    [
        SNew(SBorder)
        .BorderImage(FAppStyle::GetBrush(TEXT("WhiteBrush")))
        .BorderBackgroundColor(this, &SMyRow::GetBackgroundColor)
        .Padding(0.0f)
    ]

    // Layer 1: Content columns
    + SOverlay::Slot()
    .Padding(FMySpacing::XS, 0.0f)
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().FillWidth(1.0f)
        [
            SNew(STextBlock)
            .Text(Item->GetDisplayName())
            .Font(FMyFonts::Regular())
        ]
        + SHorizontalBox::Slot().FillWidth(1.0f)
        [
            SNew(STextBlock)
            .Text(Item->GetStatusText())
            .ColorAndOpacity(UIBind(&FMyColors::TextSecondary))
        ]
    ]

    // Layer 2: Action buttons (visible on hover, covers rightmost columns)
    + SOverlay::Slot()
    .HAlign(HAlign_Right)
    .VAlign(VAlign_Fill)
    [
        SNew(SBox)
        .Visibility(this, &SMyRow::GetActionButtonsVisibility)
        .Padding(FMySpacing::XS, 0.0f)
        [
            SNew(SHorizontalBox)
            + SHorizontalBox::Slot().AutoWidth().Padding(FMySpacing::XXS, 0.0f)
            [
                SNew(SMyIconButton)
                .Variant(EMyButtonVariant::Simple)
                .IconBrush(EditIconBrush)
                .OnClicked(this, &SMyRow::HandleEditClicked)
            ]
            + SHorizontalBox::Slot().AutoWidth().Padding(FMySpacing::XXS, 0.0f)
            [
                SNew(SMyIconButton)
                .Variant(EMyButtonVariant::Simple)
                .IconBrush(DeleteIconBrush)
                .OnClicked(this, &SMyRow::HandleDeleteClicked)
            ]
        ]
    ]
];
```

**Key pattern:** The hover layer uses `HAlign_Right` to float over the right side of the content. The background of the action buttons area should match (or be slightly opaque) so text underneath doesn't bleed through. Use `GetActionButtonsVisibility()` bound to mouse hover state.

### Hit-Test Transparency

For non-interactive overlay layers (decorations, shadows, guides), use `HitTestInvisible` so mouse events pass through to layers below:

```cpp
// Decorative overlay — visible but doesn't block clicks
+ SOverlay::Slot()
[
    SNew(SImage)
    .Image(ShadowBrush)
    .Visibility(EVisibility::HitTestInvisible)  // passes clicks through
]
```

## SListView and Table Patterns

`SListView` is the most complex composition pattern in Slate. It manages a data source, generates row widgets on demand, and handles selection state.

### Basic SListView Setup

```cpp
// Data source — the array must outlive the list view
TArray<TSharedPtr<FMyItem>> Items;
TArray<TSharedPtr<FMyItem>> FilteredItems;  // filtered subset

// Header row (optional — omit for simple lists)
TSharedPtr<SHeaderRow> HeaderRow;
HeaderRow = SNew(SHeaderRow)
    + SHeaderRow::Column(TEXT("Name"))
    .DefaultLabel(LOCTEXT("NameCol", "Name"))
    .FillWidth(1.0f)
    + SHeaderRow::Column(TEXT("Type"))
    .DefaultLabel(LOCTEXT("TypeCol", "Type"))
    .FillWidth(0.5f)
    + SHeaderRow::Column(TEXT("Status"))
    .DefaultLabel(LOCTEXT("StatusCol", "Status"))
    .FixedWidth(100.0f);

// List view
SAssignNew(ListView, SListView<TSharedPtr<FMyItem>>)
.ListItemsSource(&FilteredItems)
.OnGenerateRow(this, &SMyComposite::OnGenerateRow)
.OnSelectionChanged(this, &SMyComposite::OnSelectionChanged)
.SelectionMode(ESelectionMode::Multi)
.HeaderRow(HeaderRow);
```

### OnGenerateRow — The Row Factory

This callback creates the visual representation for each item. Return an `STableRow` wrapping your row Component.

```cpp
TSharedRef<ITableRow> SMyComposite::OnGenerateRow(
    TSharedPtr<FMyItem> Item,
    const TSharedRef<STableViewBase>& OwnerTable)
{
    return SNew(STableRow<TSharedPtr<FMyItem>>, OwnerTable)
    [
        SNew(SMyItemRow)
        .Item(Item)
        .OnEditClicked(this, &SMyComposite::HandleEditItem)
        .OnDeleteClicked(this, &SMyComposite::HandleDeleteItem)
    ];
}
```

**Key pattern:** The row widget (`SMyItemRow`) is a Component — it composes Primitives to display one item. The Composite owns the data source and handles domain events through delegates that the row fires.

### Data Updates

When the data source changes, tell the list view to regenerate:

```cpp
// After modifying Items or FilteredItems:
if (ListView.IsValid())
{
    ListView->RequestListRefresh();
}
```

`RequestListRefresh()` marks the list for regeneration on the next frame. It does not immediately rebuild — Slate batches the update.

### STreeView Extension

`STreeView` adds hierarchical data with expand/collapse:

```cpp
SNew(STreeView<TSharedPtr<FMyTreeItem>>)
.TreeItemsSource(&RootItems)
.OnGenerateRow(this, &SMyComposite::OnGenerateTreeRow)
.OnGetChildren(this, &SMyComposite::OnGetChildren)
.OnSelectionChanged(this, &SMyComposite::OnTreeSelectionChanged)

// Child provider callback:
void SMyComposite::OnGetChildren(
    TSharedPtr<FMyTreeItem> Parent,
    TArray<TSharedPtr<FMyTreeItem>>& OutChildren)
{
    OutChildren = Parent->Children;
}
```

### External Scrollbar

For custom-styled scrollbars, create an external scrollbar and bind it:

```cpp
TSharedPtr<SScrollBar> ExternalScrollbar;

SAssignNew(ExternalScrollbar, SScrollBar)
.Style(&FMySlateStyle::GetScrollBarStyle());

SNew(SHorizontalBox)
+ SHorizontalBox::Slot().FillWidth(1.0f)
[
    SAssignNew(ListView, SListView<TSharedPtr<FMyItem>>)
    .ExternalScrollbar(ExternalScrollbar)
    // ... other settings
]
+ SHorizontalBox::Slot().AutoWidth()
[
    ExternalScrollbar.ToSharedRef()
]
```

## Slot Patterns

### Default Slot (Single Child)

The simplest content injection — accepts one child widget via bracket syntax.

```cpp
// Declaration:
SLATE_DEFAULT_SLOT(FArguments, Content)

// In Construct:
ChildSlot
[
    SNew(SBorder)
    .Padding(FMySpacing::MD)
    [
        InArgs._Content.Widget
    ]
];

// Usage:
SNew(SMyPanel)
[
    SNew(STextBlock).Text(LOCTEXT("Hello", "Hello"))
]
```

### Named Slots (Multiple Injection Points)

For Layouts with fixed regions:

```cpp
// Declaration:
SLATE_NAMED_SLOT(FArguments, LeftContent)
SLATE_NAMED_SLOT(FArguments, RightContent)
SLATE_NAMED_SLOT(FArguments, BottomContent)

// In Construct:
ChildSlot
[
    SNew(SSplitter)
    + SSplitter::Slot().Value(0.3f)
    [InArgs._LeftContent.Widget]
    + SSplitter::Slot().Value(0.7f)
    [
        SNew(SVerticalBox)
        + SVerticalBox::Slot().FillHeight(1.0f)
        [InArgs._RightContent.Widget]
        + SVerticalBox::Slot().AutoHeight()
        [InArgs._BottomContent.Widget]
    ]
];

// Usage:
SNew(SMyLayout)
.LeftContent()
[
    SidebarComposite
]
.RightContent()
[
    ContentComposite
]
.BottomContent()
[
    StatusBarComposite
]
```

### Multi-Slot (Variable Children)

For dynamic numbers of children, use `SHorizontalBox` / `SVerticalBox` slot patterns directly. These are not custom slots — they use Slate's built-in panel slots.

```cpp
// Build a toolbar dynamically from a list of actions
TSharedRef<SHorizontalBox> Toolbar = SNew(SHorizontalBox);

for (const FMyAction& Action : Actions)
{
    Toolbar->AddSlot()
    .AutoWidth()
    .Padding(FMySpacing::XXS, 0.0f)
    [
        SNew(SMyIconButton)
        .Variant(EMyButtonVariant::Simple)
        .IconBrush(Action.IconBrush)
        .Text(Action.Label)
        .OnClicked(FOnClicked::CreateSP(this, &SMyToolbar::HandleAction, Action.Id))
    ];
}
```

## Widget Factory Patterns

### Conditional Widget Creation

Build widgets conditionally in `Construct` based on arguments:

```cpp
void SMyHeaderBar::Construct(const FArguments& InArgs)
{
    TSharedRef<SHorizontalBox> HeaderBox = SNew(SHorizontalBox)
        + SHorizontalBox::Slot()
        .FillWidth(1.0f)
        .VAlign(VAlign_Center)
        [
            SNew(STextBlock)
            .Text(InArgs._Title)
            .Font(FMyFonts::LargeBold())
        ];

    // Conditionally add close button
    if (InArgs._bShowCloseButton)
    {
        HeaderBox->AddSlot()
        .AutoWidth()
        .VAlign(VAlign_Center)
        [
            SNew(SMyIconButton)
            .Variant(EMyButtonVariant::NoBorder)
            .IconBrush(FAppStyle::GetBrush(TEXT("Icons.X")))
            .OnClicked(InArgs._OnCloseClicked)
        ];
    }

    ChildSlot[HeaderBox];
}
```

### SWidgetSwitcher for State Machines

Display different content based on a state enum:

```cpp
UENUM()
enum class EMyViewState : uint8
{
    Loading,
    Content,
    Empty,
    Error
};

// In Construct:
SNew(SWidgetSwitcher)
.WidgetIndex_Lambda([this]()
{
    return static_cast<int32>(CurrentState);
})
+ SWidgetSwitcher::Slot()  // Index 0: Loading
[
    SNew(SMyPanel).Variant(EMyPanelVariant::Dark)
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().HAlign(HAlign_Center)
        [SNew(SThrobber)]
    ]
]
+ SWidgetSwitcher::Slot()  // Index 1: Content
[
    ContentComposite
]
+ SWidgetSwitcher::Slot()  // Index 2: Empty
[
    SNew(SBox).HAlign(HAlign_Center).VAlign(VAlign_Center)
    [
        SNew(STextBlock)
        .Text(LOCTEXT("Empty", "No items found"))
        .Font(FMyFonts::Regular())
        .ColorAndOpacity(UIBind(&FMyColors::TextMuted))
    ]
]
+ SWidgetSwitcher::Slot()  // Index 3: Error
[
    ErrorDisplayWidget
]
```

### SAssignNew for Member Storage

When you need to reference a widget after construction (e.g., to call `RequestListRefresh()` or `SetText()`), use `SAssignNew`:

```cpp
TSharedPtr<SEditableTextBox> SearchInput;
TSharedPtr<SListView<TSharedPtr<FMyItem>>> ListView;

// In Construct:
SAssignNew(SearchInput, SEditableTextBox)
.OnTextChanged(this, &SMyWidget::HandleSearchChanged)
.HintText(LOCTEXT("SearchHint", "Search..."))

SAssignNew(ListView, SListView<TSharedPtr<FMyItem>>)
.ListItemsSource(&FilteredItems)
.OnGenerateRow(this, &SMyWidget::OnGenerateRow)
```

**Rule:** Only store widgets as members when you need to call methods on them after construction. Most widgets are fire-and-forget — build them in `Construct` and let Slate manage their lifecycle.

## SSplitter and SDockTab Patterns

These patterns are used at the Layout level to define spatial arrangement.

### SSplitter

```cpp
SNew(SSplitter)
.Orientation(Orient_Horizontal)

// Left pane — sidebar
+ SSplitter::Slot()
.Value(0.3f)
.MinSize(FMySizing::SidebarMinWidth)
[
    SidebarComposite
]

// Right pane — main content
+ SSplitter::Slot()
.Value(0.7f)
[
    ContentComposite
]
```

**Nested SSplitter** for complex layouts:

```cpp
SNew(SSplitter)
.Orientation(Orient_Horizontal)
+ SSplitter::Slot().Value(0.25f)
[Sidebar]
+ SSplitter::Slot().Value(0.75f)
[
    SNew(SSplitter)
    .Orientation(Orient_Vertical)
    + SSplitter::Slot().Value(0.7f)
    [MainContent]
    + SSplitter::Slot().Value(0.3f)
    [BottomPanel]
]
```

### SDockTab Registration

For editor tools that integrate with the docking system:

```cpp
// In your module's StartupModule:
FGlobalTabmanager::Get()->RegisterNomadTabSpawner(
    TEXT("MyToolTab"),
    FOnSpawnTab::CreateRaw(this, &FMyModule::SpawnTab))
    .SetDisplayName(LOCTEXT("MyToolTitle", "My Tool"))
    .SetMenuType(ETabSpawnerMenuType::Enabled)
    .SetIcon(FSlateIcon(FAppStyle::GetAppStyleSetName(), TEXT("Icons.Settings")));

// Tab spawner callback:
TSharedRef<SDockTab> FMyModule::SpawnTab(const FSpawnTabArgs& Args)
{
    return SNew(SDockTab)
    .TabRole(NomadTab)
    [
        SNew(SMyToolView)  // Your top-level View widget
    ];
}

// In ShutdownModule:
FGlobalTabmanager::Get()->UnregisterNomadTabSpawner(TEXT("MyToolTab"));
```

### SWindow for Standalone Windows

For standalone tool windows outside the docking system:

```cpp
TSharedRef<SWindow> Window = SNew(SWindow)
    .Title(LOCTEXT("MyToolTitle", "My Tool"))
    .ClientSize(FVector2D(800, 600))
    .MinWidth(400)
    .MinHeight(300)
    .SizingRule(ESizingRule::UserSized)
    [
        SNew(SMyToolView)
    ];

FSlateApplication::Get().AddWindow(Window);
```
