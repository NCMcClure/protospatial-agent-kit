# Slate Design Tokens

Design tokens are named constants that encode every visual decision in your Slate UI. They sit beneath the widget hierarchy as the foundation layer — no widget should contain a hardcoded color, font size, spacing value, or brush definition. Instead, widgets reference tokens, and tokens reference your design system.

In Slate, tokens take three forms based on their C++ requirements:

| Token Type | C++ Construct | Resolved At | Example |
|-----------|---------------|-------------|---------|
| Spacing, sizing, borders | `inline constexpr float` in namespace | Compile time | `FMySpacing::MD` → `8.0f` |
| Fonts | `inline` functions returning `FSlateFontInfo` | Runtime (but deterministic) | `FMyFonts::Regular()` → 10pt default |
| Colors | Semantic struct + `UIBind()` lambdas | Runtime (reactive) | `UIBind(&FMyColors::TextPrimary)` |
| Brushes | Static `FSlateBrush` members | Runtime (stable address) | `FMyStyle::GetPanelBrush(Variant)` |

## Token Layer Architecture

The token layer has three tiers, each with different mutability:

**Tier 1 — Static tokens** (spacing, sizing): Compile-time constants in namespaces. These never change at runtime. If your spacing scale changes, you recompile.

**Tier 2 — Font tokens**: Inline functions returning `FSlateFontInfo`. Not constexpr because `FSlateFontInfo` construction depends on `FCoreStyle` runtime state, but the values are deterministic — they return the same result every call.

**Tier 3 — Color tokens**: Runtime-resolved through lambdas that read from a settings object. This is the reactive layer — when a user changes their color preferences, every widget updates on the next frame without rebuilding any widget tree. This is the UIBind pattern.

## Spacing Tokens

Spacing tokens use T-shirt sizing in a constexpr namespace. The scale follows a consistent progression that maps well to Slate's padding and margin needs.

```cpp
// MySpacing.h
#pragma once

namespace FMySpacing
{
    inline constexpr float XXS  = 2.0f;
    inline constexpr float XS   = 4.0f;
    inline constexpr float SM   = 6.0f;
    inline constexpr float MD   = 8.0f;
    inline constexpr float LG   = 12.0f;
    inline constexpr float XL   = 16.0f;
    inline constexpr float XXL  = 20.0f;
    inline constexpr float XXXL = 32.0f;
}
```

**Usage in Slate syntax:**

```cpp
// Uniform padding
SNew(SBorder)
.Padding(FMySpacing::MD)  // 8px all sides

// Asymmetric padding (horizontal, vertical)
SNew(SBorder)
.Padding(FMySpacing::SM, FMySpacing::XS)  // 6px horizontal, 4px vertical

// Full FMargin
SNew(SBorder)
.Padding(FMargin(FMySpacing::MD, FMySpacing::SM, FMySpacing::MD, FMySpacing::LG))

// Slot padding
+ SHorizontalBox::Slot()
.Padding(FMySpacing::XS, 0.0f)  // 4px horizontal gap, no vertical

// Spacer widget
+ SHorizontalBox::Slot()
.AutoWidth()
[SNew(SSpacer).Size(FVector2D(FMySpacing::MD, 0.0f))]
```

T-shirt sizing is more readable in Slate code than numeric indices. `.Padding(FMySpacing::SM)` communicates intent where `.Padding(6.0f)` does not.

## Sizing Tokens

Sizing tokens define element dimensions — icon sizes, minimum widget widths, row heights, border thicknesses. Same constexpr namespace pattern.

```cpp
// MySizing.h
#pragma once

namespace FMySizing
{
    // Icon sizes
    inline constexpr float IconSM  = 14.0f;
    inline constexpr float IconMD  = 16.0f;
    inline constexpr float IconLG  = 20.0f;
    inline constexpr float IconXL  = 24.0f;

    // Widget constraints
    inline constexpr float ButtonMinWidth   = 80.0f;
    inline constexpr float RowHeight        = 28.0f;
    inline constexpr float HeaderHeight     = 36.0f;
    inline constexpr float SidebarMinWidth  = 200.0f;
    inline constexpr float ScrollbarWidth   = 8.0f;

    // Border and corner
    inline constexpr float BorderThin    = 1.0f;
    inline constexpr float BorderMedium  = 2.0f;
    inline constexpr float CornerSM      = 2.0f;
    inline constexpr float CornerMD      = 4.0f;
    inline constexpr float CornerLG      = 8.0f;
}
```

**Usage in Slate syntax:**

```cpp
// Icon sizing via FVector2D
SNew(SImage)
.Image(IconBrush)
.DesiredSizeOverride(FVector2D(FMySizing::IconMD, FMySizing::IconMD))

// Row height constraint
SNew(SBox)
.HeightOverride(FMySizing::RowHeight)
[RowContent]

// Minimum width constraint
SNew(SBox)
.MinDesiredWidth(FMySizing::ButtonMinWidth)
[ButtonContent]

// Fixed column width in SHeaderRow
+ SHeaderRow::Column(TEXT("Status"))
.FixedWidth(FMySizing::ColumnStatusWidth)
```

**Sizing vs spacing distinction**: Sizing tokens describe element dimensions (how big is this thing?). Spacing tokens describe gaps between elements (how far apart are these things?). A row height is sizing. The padding inside that row is spacing.

## Font Tokens

Font tokens are inline functions because `FSlateFontInfo` depends on `FCoreStyle` which requires engine initialization. The functions are deterministic — they return the same value every call — but cannot be constexpr.

```cpp
// MyFonts.h
#pragma once

#include "Styling/CoreStyle.h"

namespace FMyFonts
{
    inline FSlateFontInfo Tiny()
    {
        return FCoreStyle::GetDefaultFontStyle("Regular", 8);
    }

    inline FSlateFontInfo Small()
    {
        return FCoreStyle::GetDefaultFontStyle("Regular", 9);
    }

    inline FSlateFontInfo Regular()
    {
        return FCoreStyle::GetDefaultFontStyle("Regular", 10);
    }

    inline FSlateFontInfo RegularBold()
    {
        return FCoreStyle::GetDefaultFontStyle("Bold", 10);
    }

    inline FSlateFontInfo Large()
    {
        return FCoreStyle::GetDefaultFontStyle("Regular", 12);
    }

    inline FSlateFontInfo LargeBold()
    {
        return FCoreStyle::GetDefaultFontStyle("Bold", 12);
    }

    inline FSlateFontInfo Heading()
    {
        return FCoreStyle::GetDefaultFontStyle("Bold", 14);
    }

    inline FSlateFontInfo HeadingLarge()
    {
        return FCoreStyle::GetDefaultFontStyle("Bold", 18);
    }

    inline FSlateFontInfo Mono()
    {
        return FCoreStyle::GetDefaultFontStyle("Mono", 10);
    }

    inline FSlateFontInfo MonoSmall()
    {
        return FCoreStyle::GetDefaultFontStyle("Mono", 9);
    }
}
```

**Usage in Slate syntax:**

```cpp
SNew(STextBlock)
.Text(FText::FromString(TEXT("Section Title")))
.Font(FMyFonts::LargeBold())
.ColorAndOpacity(UIBind(&FMyColors::TextPrimary))
```

**Custom fonts**: If your project ships custom font assets, modify the factory functions to load from your font asset path instead of `FCoreStyle`:

```cpp
inline FSlateFontInfo Regular()
{
    return FSlateFontInfo(
        FPaths::EngineContentDir() / TEXT("Slate/Fonts/MyCustomFont.ttf"),
        10
    );
}
```

## Color Tokens

Color tokens are the most architecturally significant token type. They enable live theme updates without rebuilding widget trees.

### Semantic Color Struct

Define a struct with semantically named color members. This struct lives in your settings class (typically a `UDeveloperSettings` subclass) so users can customize colors via the editor's project settings panel.

```cpp
// MyColors.h
#pragma once

#include "CoreMinimal.h"
#include "MyColors.generated.h"

USTRUCT()
struct FMyColors
{
    GENERATED_BODY()

    // Backgrounds
    UPROPERTY(EditAnywhere, Category = "Background")
    FColor BgPrimary = FColor(30, 30, 30);

    UPROPERTY(EditAnywhere, Category = "Background")
    FColor BgSecondary = FColor(40, 40, 40);

    UPROPERTY(EditAnywhere, Category = "Background")
    FColor BgPanel = FColor(50, 50, 50);

    UPROPERTY(EditAnywhere, Category = "Background")
    FColor BgPanelDark = FColor(35, 35, 35);

    UPROPERTY(EditAnywhere, Category = "Background")
    FColor BgOverlay = FColor(20, 20, 20);

    // Text
    UPROPERTY(EditAnywhere, Category = "Text")
    FColor TextPrimary = FColor(220, 220, 220);

    UPROPERTY(EditAnywhere, Category = "Text")
    FColor TextSecondary = FColor(160, 160, 160);

    UPROPERTY(EditAnywhere, Category = "Text")
    FColor TextMuted = FColor(100, 100, 100);

    // Buttons
    UPROPERTY(EditAnywhere, Category = "Buttons")
    FColor BtnNormal = FColor(60, 60, 60);

    UPROPERTY(EditAnywhere, Category = "Buttons")
    FColor BtnHovered = FColor(80, 80, 80);

    UPROPERTY(EditAnywhere, Category = "Buttons")
    FColor BtnPressed = FColor(45, 45, 45);

    UPROPERTY(EditAnywhere, Category = "Buttons")
    FColor BtnDisabled = FColor(40, 40, 40);

    UPROPERTY(EditAnywhere, Category = "Buttons")
    FColor BtnForeground = FColor(200, 200, 200);

    // Accents
    UPROPERTY(EditAnywhere, Category = "Accents")
    FColor AccentPrimary = FColor(56, 132, 244);

    UPROPERTY(EditAnywhere, Category = "Accents")
    FColor AccentSuccess = FColor(76, 175, 80);

    UPROPERTY(EditAnywhere, Category = "Accents")
    FColor AccentWarning = FColor(255, 183, 77);

    UPROPERTY(EditAnywhere, Category = "Accents")
    FColor AccentError = FColor(229, 57, 53);

    // Borders
    UPROPERTY(EditAnywhere, Category = "Borders")
    FColor BorderDefault = FColor(65, 65, 65);

    UPROPERTY(EditAnywhere, Category = "Borders")
    FColor BorderFocused = FColor(56, 132, 244);

    // Conversion helpers
    static FLinearColor ToLinear(const FColor& Color)
    {
        return Color.ReinterpretAsLinear();
    }

    static FLinearColor ToLinearWithAlpha(const FColor& Color, float Alpha)
    {
        FLinearColor Linear = Color.ReinterpretAsLinear();
        Linear.A = Alpha;
        return Linear;
    }
};
```

**Naming convention**: Color names use `[Context][Purpose]` — `BgPanel` (background for panels), `TextPrimary` (primary text color), `AccentPrimary` (primary accent). The context groups colors by where they're used. The purpose distinguishes variants within a context.

### The UIBind Pattern

UIBind is the reactive binding mechanism. It creates `TAttribute<FSlateColor>` instances that read from your settings object every frame. When the user changes a color in settings, every bound widget updates immediately — no widget rebuild needed.

```cpp
// In your settings header or a dedicated UIBindings.h

// Basic color binding — reads the color member from settings every frame
inline TAttribute<FSlateColor> UIBind(FColor FMyColors::* Member)
{
    return TAttribute<FSlateColor>::CreateLambda([Member]() -> FSlateColor
    {
        const UMySettings* Settings = GetDefault<UMySettings>();
        return FSlateColor(FMyColors::ToLinear(Settings->UIColors.*Member));
    });
}

// Color binding with alpha override — same reactive read, custom opacity
inline TAttribute<FSlateColor> UIBindAlpha(FColor FMyColors::* Member, float Alpha)
{
    return TAttribute<FSlateColor>::CreateLambda([Member, Alpha]() -> FSlateColor
    {
        const UMySettings* Settings = GetDefault<UMySettings>();
        return FSlateColor(FMyColors::ToLinearWithAlpha(Settings->UIColors.*Member, Alpha));
    });
}
```

**How it works**: `FColor FMyColors::* Member` is a pointer-to-member. It doesn't point to a specific color value — it points to a *slot* in the `FMyColors` struct. The lambda captures this slot reference and reads the actual value from the current settings instance at call time. This is the indirection that enables reactivity: the widget doesn't know which color it's using, only which semantic slot to read from.

**Usage in widgets:**

```cpp
// In any widget's Construct method:

// Text color
SNew(STextBlock)
.ColorAndOpacity(UIBind(&FMyColors::TextPrimary))

// Border background
SNew(SBorder)
.BorderBackgroundColor(UIBind(&FMyColors::BgPanel))

// Semi-transparent overlay
SNew(SBorder)
.BorderBackgroundColor(UIBindAlpha(&FMyColors::BgOverlay, 0.85f))

// Button foreground
SNew(SButton)
.ForegroundColor(UIBind(&FMyColors::BtnForeground))
```

**Performance**: The lambda is called every frame during Slate's paint pass. `GetDefault<>()` is a fast CDO lookup, and member pointer dereference is a single offset — this is negligible cost. Do not cache the result; the whole point is to re-read every frame.

### Alternative: Non-Settings Color Source

If you don't use `UDeveloperSettings` (e.g., runtime UI with a custom theme manager), adapt UIBind to read from your source:

```cpp
inline TAttribute<FSlateColor> UIBind(FColor FMyColors::* Member)
{
    return TAttribute<FSlateColor>::CreateLambda([Member]() -> FSlateColor
    {
        const FMyColors& Colors = FMyThemeManager::Get().GetCurrentTheme();
        return FSlateColor(FMyColors::ToLinear(Colors.*Member));
    });
}
```

The pattern is the same — member pointer indirection + runtime read. Only the source changes.

## Brush Tokens

`FSlateBrush` instances require stable memory addresses because Slate stores `const FSlateBrush*` pointers. Brushes that go out of scope while Slate holds a pointer will crash.

Three approaches, each suited to different use cases:

### Static Members in the Style Set

The most common approach. Brushes live as static members of your `FSlateStyleSet` subclass. See `style-architecture.md` for the full pattern.

```cpp
// In FMySlateStyle (your style set class)
static FSlateRoundedBoxBrush PanelBrush_Light;
static FSlateRoundedBoxBrush PanelBrush_Dark;

// Constructed during style initialization
PanelBrush_Light = FSlateRoundedBoxBrush(
    FMyColors::ToLinear(Settings->UIColors.BgPanel),
    FMySizing::CornerMD  // corner radius from sizing tokens
);
```

### FSlateRoundedBoxBrush for Procedural Shapes

Creates rounded rectangles without texture assets. Ideal for panels, buttons, and card backgrounds.

```cpp
// Solid rounded rect
FSlateRoundedBoxBrush SolidBrush(
    FLinearColor(0.2f, 0.2f, 0.2f, 1.0f),  // fill color
    4.0f                                       // corner radius
);

// Rounded rect with outline
FSlateRoundedBoxBrush OutlinedBrush(
    FLinearColor(0.2f, 0.2f, 0.2f, 1.0f),  // fill color
    4.0f,                                     // corner radius
    FLinearColor(0.4f, 0.4f, 0.4f, 1.0f),  // outline color
    1.0f                                      // outline width
);
```

### FSlateColorBrush for Solid Fills

Lightweight alternative when you don't need rounded corners.

```cpp
FSlateColorBrush FlatBrush(FLinearColor(0.2f, 0.2f, 0.2f, 1.0f));
```

### FSlateNoResource for Invisible Elements

Used for button styles that should be visually invisible (e.g., NoBorder variant).

```cpp
// No visual — used for button normal state in transparent variants
FSlateNoResource()
```

## Token File Organization

Recommended directory layout for the token layer:

```
Source/MyModule/
└── UI/
    ├── Tokens/
    │   ├── MySpacing.h      // FMySpacing namespace
    │   ├── MyFonts.h        // FMyFonts namespace
    │   ├── MySizing.h       // FMySizing namespace
    │   └── MyColors.h       // FMyColors struct + UIBind functions
    ├── Style/
    │   ├── MySlateStyle.h   // FSlateStyleSet subclass (see style-architecture.md)
    │   └── MySlateStyle.cpp
    └── Widgets/
        ├── Primitives/
        ├── Components/
        ├── Composites/
        ├── Layouts/
        └── Views/
```

The token files are header-only (`inline constexpr`, `inline` functions, `TAttribute::CreateLambda`). No .cpp files needed. Include them where used — the compiler inlines everything.

## When to Add a New Token

If you find yourself writing any of these in a widget's `Construct` method, a token is missing:

| You wrote... | Add a token to... |
|-------------|-------------------|
| `FMargin(8.0f)` | `FMySpacing` namespace |
| `FLinearColor(0.2f, 0.2f, 0.2f, 1.0f)` | `FMyColors` struct |
| `FCoreStyle::GetDefaultFontStyle("Regular", 10)` | `FMyFonts` namespace |
| `FVector2D(16.0f, 16.0f)` for icon size | `FMySizing` namespace |
| `.FixedWidth(120.0f)` | `FMySizing` namespace |

Never add a one-off value. If a value is truly unique to one widget, question whether the design is consistent. A design system with 47 unique spacing values is not a system.

**Exception**: Layout-specific ratios (`SSplitter::Slot().Value(0.3f)`) are not tokens. Splitter ratios describe proportional relationships, not reusable spacing values.
