# Slate Style Architecture

The `FSlateStyleSet` is the central registry for all visual style definitions in a Slate UI. It provides named `FSlateBrush`, `FButtonStyle`, `FTextBlockStyle`, `FCheckBoxStyle`, and other style structs that widgets reference by stable pointer. This architecture enables live style updates, variant-driven styling, and consistent visual identity across your entire widget hierarchy.

## Why a Central Style Set

**Stable addresses.** Slate takes `const FSlateBrush*` and `const FButtonStyle*` by pointer. These pointers must remain valid for the lifetime of the widget. A central style set with static or long-lived member data guarantees stable addresses. Local brushes created on the stack in `Construct` will crash when Slate tries to paint them.

**Single source of truth.** All visual definitions live in one class. Change a brush definition and every widget referencing it updates. No hunting through widget files for hardcoded colors.

**Live updates.** The style set can regenerate its styles when settings change. Because Slate re-reads from the same pointer addresses on each paint pass, the updated values appear on the next frame — no widget rebuild needed.

**Discoverability.** A new developer can read the style set header and see every visual variant the system offers. This prevents "I didn't know we had a secondary button style" duplication.

## The FSlateStyleSet Pattern

### Header

```cpp
// MySlateStyle.h
#pragma once

#include "Styling/SlateStyle.h"

class FMySlateStyle : public FSlateStyleSet
{
public:
    FMySlateStyle();
    virtual ~FMySlateStyle();

    /** Register with FSlateStyleRegistry. Call during module startup. */
    static void Initialize();

    /** Unregister. Call during module shutdown. */
    static void Shutdown();

    /** Access the singleton instance. Only valid between Initialize/Shutdown. */
    static const FMySlateStyle& Get();

    // --- Style accessors ---

    /** Panel border brush by variant. */
    static const FSlateBrush& GetPanelBrush(EMyPanelVariant Variant);

    /** Button style by variant. */
    static const FButtonStyle& GetButtonStyle(EMyButtonVariant Variant);

    /** Checkbox style. */
    static const FCheckBoxStyle& GetCheckBoxStyle();

    /** Header row style. */
    static const FHeaderRowStyle& GetHeaderRowStyle();

    /** Scrollbar style. */
    static const FScrollBarStyle& GetScrollBarStyle();

    /** Re-read colors from settings and rebuild all styles. */
    static void UpdateStyles();

private:
    void CreatePanelStyles();
    void CreateButtonStyles();
    void CreateCheckBoxStyle();
    void CreateHeaderRowStyle();
    void CreateScrollBarStyle();

    // --- Static style instances (stable addresses) ---

    // Panel brushes
    static FSlateRoundedBoxBrush PanelBrush_Light;
    static FSlateRoundedBoxBrush PanelBrush_Dark;
    static FSlateRoundedBoxBrush PanelBrush_Overlay;

    // Button styles
    static FButtonStyle ButtonStyle_Standard;
    static FButtonStyle ButtonStyle_Simple;
    static FButtonStyle ButtonStyle_NoBorder;

    // Other styles
    static FCheckBoxStyle CheckBoxStyle;
    static FHeaderRowStyle HeaderRowStyle;
    static FScrollBarStyle ScrollBarStyle;

    static TSharedPtr<FMySlateStyle> Instance;
};
```

### Implementation

```cpp
// MySlateStyle.cpp
#include "Style/MySlateStyle.h"
#include "Styling/SlateStyleRegistry.h"
#include "Styling/SlateTypes.h"
#include "Styling/StyleColors.h"
#include "Tokens/MySpacing.h"
#include "Tokens/MySizing.h"
#include "Tokens/MyColors.h"
#include "MySettings.h"

// Static member definitions
TSharedPtr<FMySlateStyle> FMySlateStyle::Instance;
FSlateRoundedBoxBrush FMySlateStyle::PanelBrush_Light;
FSlateRoundedBoxBrush FMySlateStyle::PanelBrush_Dark;
FSlateRoundedBoxBrush FMySlateStyle::PanelBrush_Overlay;
FButtonStyle FMySlateStyle::ButtonStyle_Standard;
FButtonStyle FMySlateStyle::ButtonStyle_Simple;
FButtonStyle FMySlateStyle::ButtonStyle_NoBorder;
FCheckBoxStyle FMySlateStyle::CheckBoxStyle;
FHeaderRowStyle FMySlateStyle::HeaderRowStyle;
FScrollBarStyle FMySlateStyle::ScrollBarStyle;

FMySlateStyle::FMySlateStyle()
    : FSlateStyleSet(TEXT("MySlateStyle"))
{
    CreatePanelStyles();
    CreateButtonStyles();
    CreateCheckBoxStyle();
    CreateHeaderRowStyle();
    CreateScrollBarStyle();
}

FMySlateStyle::~FMySlateStyle()
{
}

void FMySlateStyle::Initialize()
{
    if (!Instance.IsValid())
    {
        Instance = MakeShareable(new FMySlateStyle());
        FSlateStyleRegistry::RegisterSlateStyle(*Instance);
    }
}

void FMySlateStyle::Shutdown()
{
    if (Instance.IsValid())
    {
        FSlateStyleRegistry::UnRegisterSlateStyle(*Instance);
        Instance.Reset();
    }
}

const FMySlateStyle& FMySlateStyle::Get()
{
    check(Instance.IsValid());
    return *Instance;
}

void FMySlateStyle::UpdateStyles()
{
    if (Instance.IsValid())
    {
        Instance->CreatePanelStyles();
        Instance->CreateButtonStyles();
        Instance->CreateCheckBoxStyle();
        Instance->CreateHeaderRowStyle();
        Instance->CreateScrollBarStyle();
    }
}
```

**Key points:**
- The style set name (`TEXT("MySlateStyle")`) must be unique across the engine. Use your project prefix.
- `Initialize()` and `Shutdown()` are called from your module's `StartupModule()` and `ShutdownModule()`.
- Static members are defined in the .cpp to ensure single definition across translation units.
- `Get()` uses `check()` — calling it before `Initialize()` is a programming error.

## Widget Variant System

Variants replace inheritance. Instead of `SMyButton`, `SMySimpleButton`, and `SMyNoBorderButton` (three classes with duplicated logic), use one widget class with a variant enum that selects from the style set.

### Variant Enums

```cpp
// MyWidgetTypes.h
#pragma once

UENUM()
enum class EMyButtonVariant : uint8
{
    /** Solid background, visible borders. Default for primary actions. */
    Standard,

    /** Transparent normal state, semi-transparent hover. For toolbar icons. */
    Simple,

    /** Completely invisible. For inline actions like close buttons. */
    NoBorder
};

UENUM()
enum class EMyPanelVariant : uint8
{
    /** Light background for content areas. */
    Light,

    /** Dark background for sidebars and headers. */
    Dark,

    /** Semi-transparent for overlay panels. */
    Overlay
};
```

### Variant in SLATE_BEGIN_ARGS

```cpp
class SMyIconButton : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SMyIconButton)
        : _Variant(EMyButtonVariant::Standard)
    {}
        SLATE_ARGUMENT(EMyButtonVariant, Variant)
        SLATE_ARGUMENT(const FSlateBrush*, IconBrush)
        SLATE_ATTRIBUTE(FText, Text)
        SLATE_ATTRIBUTE(FVector2D, IconSize)
        SLATE_EVENT(FOnClicked, OnClicked)
    SLATE_END_ARGS()

    void Construct(const FArguments& InArgs);
};
```

### Variant Resolution in Construct

```cpp
void SMyIconButton::Construct(const FArguments& InArgs)
{
    // Variant selects the style — no conditional logic in the widget
    const FButtonStyle& Style = FMySlateStyle::GetButtonStyle(InArgs._Variant);

    ChildSlot
    [
        SNew(SButton)
        .ButtonStyle(&Style)
        .OnClicked(InArgs._OnClicked)
        [
            // ... button content (icon + optional text)
        ]
    ];
}
```

**Why variants beat inheritance:**
- One widget class to maintain, test, and document
- The style set is the single source of visual variation — not scattered across widget subclasses
- Adding a new variant is one enum value + one style definition, not a new class
- Widgets stay thin — they compose Slate primitives and route to the style set, nothing more

## Style Creation Internals

### Panel Brush Styles

```cpp
void FMySlateStyle::CreatePanelStyles()
{
    const UMySettings* Settings = GetDefault<UMySettings>();
    const FMyColors& Colors = Settings->UIColors;

    PanelBrush_Light = FSlateRoundedBoxBrush(
        FMyColors::ToLinear(Colors.BgPanel),
        FMySizing::CornerMD,                      // corner radius
        FMyColors::ToLinear(Colors.BorderDefault), // outline color
        FMySizing::BorderThin                      // outline width
    );

    PanelBrush_Dark = FSlateRoundedBoxBrush(
        FMyColors::ToLinear(Colors.BgPanelDark),
        FMySizing::CornerMD,
        FMyColors::ToLinear(Colors.BorderDefault),
        FMySizing::BorderThin
    );

    FLinearColor OverlayColor = FMyColors::ToLinear(Colors.BgOverlay);
    OverlayColor.A = 0.9f;
    PanelBrush_Overlay = FSlateRoundedBoxBrush(
        OverlayColor,
        FMySizing::CornerMD
    );
}

const FSlateBrush& FMySlateStyle::GetPanelBrush(EMyPanelVariant Variant)
{
    switch (Variant)
    {
    case EMyPanelVariant::Light:   return PanelBrush_Light;
    case EMyPanelVariant::Dark:    return PanelBrush_Dark;
    case EMyPanelVariant::Overlay: return PanelBrush_Overlay;
    default:                       return PanelBrush_Light;
    }
}
```

### Button Styles

Each button variant defines all four interaction states: Normal, Hovered, Pressed, Disabled.

```cpp
void FMySlateStyle::CreateButtonStyles()
{
    const UMySettings* Settings = GetDefault<UMySettings>();
    const FMyColors& Colors = Settings->UIColors;

    // --- Standard: solid background, visible in all states ---
    ButtonStyle_Standard
        .SetNormal(FSlateRoundedBoxBrush(
            FMyColors::ToLinear(Colors.BtnNormal), FMySizing::CornerMD))
        .SetHovered(FSlateRoundedBoxBrush(
            FMyColors::ToLinear(Colors.BtnHovered), FMySizing::CornerMD))
        .SetPressed(FSlateRoundedBoxBrush(
            FMyColors::ToLinear(Colors.BtnPressed), FMySizing::CornerMD))
        .SetDisabled(FSlateRoundedBoxBrush(
            FMyColors::ToLinear(Colors.BtnDisabled), FMySizing::CornerMD))
        .SetNormalForeground(FSlateColor(FMyColors::ToLinear(Colors.BtnForeground)))
        .SetHoveredForeground(FSlateColor(FMyColors::ToLinear(Colors.BtnForeground)))
        .SetPressedForeground(FSlateColor(FMyColors::ToLinear(Colors.BtnForeground)))
        .SetDisabledForeground(FSlateColor(FMyColors::ToLinear(Colors.TextMuted)))
        .SetNormalPadding(FMargin(FMySpacing::MD, FMySpacing::XS))
        .SetPressedPadding(FMargin(FMySpacing::MD, FMySpacing::XS));

    // --- Simple: transparent normal, semi-transparent hover ---
    ButtonStyle_Simple
        .SetNormal(FSlateNoResource())
        .SetHovered(FSlateRoundedBoxBrush(
            FMyColors::ToLinearWithAlpha(Colors.BtnHovered, 0.5f), FMySizing::CornerMD))
        .SetPressed(FSlateRoundedBoxBrush(
            FMyColors::ToLinearWithAlpha(Colors.BtnPressed, 0.5f), FMySizing::CornerMD))
        .SetDisabled(FSlateNoResource())
        .SetNormalForeground(FSlateColor(FMyColors::ToLinear(Colors.TextSecondary)))
        .SetHoveredForeground(FSlateColor(FMyColors::ToLinear(Colors.TextPrimary)))
        .SetPressedForeground(FSlateColor(FMyColors::ToLinear(Colors.TextPrimary)))
        .SetDisabledForeground(FSlateColor(FMyColors::ToLinear(Colors.TextMuted)))
        .SetNormalPadding(FMargin(FMySpacing::XS))
        .SetPressedPadding(FMargin(FMySpacing::XS));

    // --- NoBorder: invisible in all states, for inline close/dismiss ---
    ButtonStyle_NoBorder
        .SetNormal(FSlateNoResource())
        .SetHovered(FSlateNoResource())
        .SetPressed(FSlateNoResource())
        .SetDisabled(FSlateNoResource())
        .SetNormalForeground(FSlateColor(FMyColors::ToLinear(Colors.TextSecondary)))
        .SetHoveredForeground(FSlateColor(FMyColors::ToLinear(Colors.TextPrimary)))
        .SetPressedForeground(FSlateColor(FMyColors::ToLinear(Colors.TextPrimary)))
        .SetDisabledForeground(FSlateColor(FMyColors::ToLinear(Colors.TextMuted)))
        .SetNormalPadding(FMargin(0.0f))
        .SetPressedPadding(FMargin(0.0f));
}

const FButtonStyle& FMySlateStyle::GetButtonStyle(EMyButtonVariant Variant)
{
    switch (Variant)
    {
    case EMyButtonVariant::Standard: return ButtonStyle_Standard;
    case EMyButtonVariant::Simple:   return ButtonStyle_Simple;
    case EMyButtonVariant::NoBorder: return ButtonStyle_NoBorder;
    default:                         return ButtonStyle_Standard;
    }
}
```

### Checkbox, Header Row, and Scrollbar

Follow the same pattern: static member, `Create*` method reads from tokens/settings, accessor returns const reference.

```cpp
void FMySlateStyle::CreateCheckBoxStyle()
{
    const UMySettings* Settings = GetDefault<UMySettings>();
    const FMyColors& Colors = Settings->UIColors;

    CheckBoxStyle = FCheckBoxStyle()
        .SetCheckBoxType(ESlateCheckBoxType::CheckBox)
        .SetUncheckedImage(FSlateRoundedBoxBrush(
            FLinearColor::Transparent, FMySizing::CornerSM,
            FMyColors::ToLinear(Colors.BorderDefault), FMySizing::BorderThin))
        .SetUncheckedHoveredImage(FSlateRoundedBoxBrush(
            FLinearColor::Transparent, FMySizing::CornerSM,
            FMyColors::ToLinear(Colors.BorderFocused), FMySizing::BorderThin))
        .SetCheckedImage(FSlateRoundedBoxBrush(
            FMyColors::ToLinear(Colors.AccentPrimary), FMySizing::CornerSM))
        .SetCheckedHoveredImage(FSlateRoundedBoxBrush(
            FMyColors::ToLinear(Colors.AccentPrimary), FMySizing::CornerSM,
            FMyColors::ToLinear(Colors.BorderFocused), FMySizing::BorderThin));
}
```

## Live Update Mechanism

When the user changes colors in settings, the style set regenerates all styles at the same memory addresses. Slate re-reads the pointer values on the next paint pass and renders the updated visuals.

```cpp
// In your module or settings class — wire the settings change delegate
void FMyModule::StartupModule()
{
    FMySlateStyle::Initialize();

    // Listen for settings changes
    if (UMySettings* Settings = GetMutableDefault<UMySettings>())
    {
        Settings->OnSettingChanged().AddLambda([](UObject*, FPropertyChangedEvent&)
        {
            FMySlateStyle::UpdateStyles();
        });
    }
}
```

**How it works:** `UpdateStyles()` calls all `Create*` methods again. These methods re-read the current color values from settings and write new brush/style data into the same static member addresses. Since Slate holds `const FSlateBrush*` pointing to those addresses, the next frame paints with the new values. No widget destruction, no `Invalidate()` calls, no tree walks.

**What about brushes?** `FSlateRoundedBoxBrush` uses assignment operators that update the internal texture resource. Assigning a new `FSlateRoundedBoxBrush` to an existing static member replaces the brush data at the same address. Slate's rendering pipeline picks up the change.

## FSlateStyleRegistry Integration

### Module Startup/Shutdown

```cpp
void FMyModule::StartupModule()
{
    FMySlateStyle::Initialize();
    // ... other initialization
}

void FMyModule::ShutdownModule()
{
    // ... other cleanup
    FMySlateStyle::Shutdown();
}
```

The style set must be registered before any widget that references it is created, and unregistered after all such widgets are destroyed. Module startup/shutdown is the natural place for this.

### Named Style Access

While `FMySlateStyle::Get()` is the preferred access pattern (direct, type-safe), the FSlateStyleRegistry also supports named lookup:

```cpp
// Not recommended for hot paths — use Get() instead
const ISlateStyle* Style = FSlateStyleRegistry::FindSlateStyle(TEXT("MySlateStyle"));
```

Named lookup is useful for cross-module access when you can't include the style set header. For your own module's widgets, always use the static `Get()` accessor.

## Editor vs Runtime Considerations

### Editor Tools

Editor tools can leverage existing UE5 editor styles as a base:

- `FAppStyle::Get()` provides editor-consistent brushes and styles
- `FCoreStyle::Get()` provides minimal foundational styles
- `FSlateIcon(FAppStyle::GetAppStyleSetName(), TEXT("Icons.X"))` accesses editor icon brushes
- Module dependency: `EditorStyle` (or `EditorFramework` in newer engine versions)

When building editor tools, decide whether to extend the editor's visual language or create a distinct custom appearance. For standalone tool windows, a custom style set creates visual identity. For detail customizations and inline editor extensions, matching `FAppStyle` is usually better.

### Runtime Slate

Runtime Slate UIs (non-editor, shipped with the game) cannot depend on `EditorStyle`:

- Use `FCoreStyle::Get()` for basic styles, or ship your own entirely
- Bundle any custom texture assets (brushes, icons) in your module's content
- `FSlateRoundedBoxBrush` and `FSlateColorBrush` generate brushes procedurally — no texture assets needed for solid colors and rounded rects
- Verify your Build.cs does not include editor-only module dependencies

### Hybrid Approach

For plugins that work in both editor and runtime contexts, guard editor-style access:

```cpp
#if WITH_EDITOR
    const FSlateBrush* IconBrush = FAppStyle::GetBrush(TEXT("Icons.Settings"));
#else
    const FSlateBrush* IconBrush = GetCustomSettingsIconBrush();
#endif
```

## Common Pitfalls

**Local FSlateBrush going out of scope.** The most common crash. If you construct a `FSlateRoundedBoxBrush` as a local variable in `Construct` and pass its address to an `SBorder`, the brush is destroyed when `Construct` returns. Slate paints garbage or crashes. Always use static or member storage with stable addresses.

**Forgetting UpdateStyles() on settings change.** You change colors in project settings, nothing happens in the UI. You need to wire the settings change delegate to `UpdateStyles()`. The UIBind color pattern handles colors reactively, but brush-based styles (panel borders, button backgrounds) need explicit regeneration.

**FSlateStyleRegistry lookup in hot paths.** `FindSlateStyle()` does a map lookup by name. Fine for initialization, but don't call it every frame from `OnPaint`. Cache the result or use the static `Get()` accessor.

**Wrong DrawAs type on FSlateRoundedBoxBrush.** `FSlateRoundedBoxBrush` sets `DrawAs` to `ESlateBrushDrawType::RoundedBox` internally. If you manually modify `DrawAs` after construction, the rounded corners disappear. Don't touch `DrawAs` on rounded box brushes.

**Not calling Shutdown before module unload.** If your module unloads without calling `FSlateStyleRegistry::UnRegisterSlateStyle`, the registry holds a dangling pointer. Subsequent `FindSlateStyle` calls for other style sets may crash or return corrupted data. Always pair `Initialize()` with `Shutdown()`.
