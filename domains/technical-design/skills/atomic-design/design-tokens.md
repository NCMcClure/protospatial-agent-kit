# Design Tokens: The Sub-Atomic Foundation Layer

Design tokens are named constants that store the fundamental visual design decisions of a system.
They sit beneath atoms as a sub-atomic layer — every atom references tokens rather than hard-coded
values. This separation enables theming, multi-brand support, platform portability, and guaranteed
visual consistency. Jina Anne pioneered the concept at Salesforce in 2014, and Brad Frost has since
embraced tokens as an essential extension to atomic design.

## What Design Tokens Represent

Tokens capture every visual decision that components should not make independently. The categories
below represent the minimum token set for any atomic design system.

### Color Tokens

Color tokens encode the palette and its semantic mapping. Structure them in two tiers: a reference
palette (the raw color values) and a semantic layer (how those colors are used).

Reference palette tokens define the raw colors: `color.blue.500`, `color.gray.100`, `color.red.600`.
These are the canonical color values and should rarely be referenced directly by components.

Semantic tokens map reference colors to purposes: `color.primary`, `color.primary.hover`,
`color.background`, `color.surface`, `color.text.primary`, `color.text.secondary`,
`color.border.default`, `color.error`, `color.success`, `color.warning`, `color.info`.

Components reference semantic tokens exclusively. This means swapping a theme requires only changing
the semantic-to-reference mapping, not touching any component code.

### Typography Tokens

Typography tokens define the type system: `font.family.heading`, `font.family.body`,
`font.family.mono`, `font.size.xs` through `font.size.4xl`, `font.weight.regular`,
`font.weight.medium`, `font.weight.bold`, `font.lineHeight.tight`, `font.lineHeight.normal`,
`font.lineHeight.relaxed`, `font.letterSpacing.tight`, `font.letterSpacing.normal`.

Composite typography tokens combine related properties for convenience: `typography.heading.xl`
might expand to `{ family: heading, size: 2xl, weight: bold, lineHeight: tight }`.

### Spacing Tokens

Spacing tokens define a consistent spatial scale. Use a base unit (typically 4px or 8px) with
named increments: `spacing.0` (0), `spacing.1` (4px), `spacing.2` (8px), `spacing.3` (12px),
`spacing.4` (16px), `spacing.6` (24px), `spacing.8` (32px), `spacing.12` (48px), `spacing.16`
(64px), `spacing.24` (96px).

Some systems add semantic spacing tokens: `spacing.inline` (horizontal space between inline
elements), `spacing.stack` (vertical space between stacked elements), `spacing.inset` (padding
inside a container).

### Border and Radius Tokens

`border.width.thin` (1px), `border.width.medium` (2px), `border.width.thick` (4px).
`border.radius.none` (0), `border.radius.sm` (4px), `border.radius.md` (8px),
`border.radius.lg` (16px), `border.radius.full` (9999px).
`border.color.default`, `border.color.focus`, `border.color.error`.

### Shadow and Elevation Tokens

`shadow.none`, `shadow.sm`, `shadow.md`, `shadow.lg`, `shadow.xl`.
Each maps to a full box-shadow value. Higher elevation implies more prominence. Use these to
create consistent depth relationships across the system.

### Motion Tokens

`motion.duration.fast` (100ms), `motion.duration.normal` (200ms), `motion.duration.slow` (400ms).
`motion.easing.default` (ease-in-out), `motion.easing.enter` (ease-out), `motion.easing.exit`
(ease-in). `motion.easing.spring` (cubic-bezier values for spring-like motion).

### Breakpoint Tokens

`breakpoint.sm` (640px), `breakpoint.md` (768px), `breakpoint.lg` (1024px), `breakpoint.xl`
(1280px), `breakpoint.2xl` (1536px). Responsive behavior at every atomic level references
these breakpoints.

### Z-Index Tokens

`zIndex.base` (0), `zIndex.dropdown` (1000), `zIndex.sticky` (1100), `zIndex.modal` (1300),
`zIndex.popover` (1400), `zIndex.tooltip` (1500), `zIndex.toast` (1600).

---

## Token Naming Conventions

Use a consistent, hierarchical naming structure across all tokens. The pattern is:
`category.property.variant.state`

Examples: `color.primary.default`, `color.primary.hover`, `font.size.lg`, `spacing.4`,
`shadow.md`, `border.radius.sm`.

Use dot notation or kebab-case depending on the format. In CSS custom properties, dots become
dashes: `--color-primary-default`. In JSON/YAML token files, use dot-delimited keys or nested
objects.

Avoid abbreviations that are not universally understood. `bg` is acceptable for background (widely
used), but `typ` for typography is not. When in doubt, spell it out.

---

## Token File Formats

### CSS Custom Properties (Simplest — works everywhere)

```css
:root {
  /* Color — Reference palette */
  --color-blue-500: #3b82f6;
  --color-gray-100: #f3f4f6;

  /* Color — Semantic */
  --color-primary: var(--color-blue-500);
  --color-background: var(--color-gray-100);

  /* Typography */
  --font-family-heading: 'Inter', sans-serif;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

Atoms consume tokens directly: `background-color: var(--color-primary);`

### JSON/YAML (Platform-Agnostic — for multi-platform systems)

```json
{
  "color": {
    "primary": {
      "value": "{color.blue.500}",
      "type": "color",
      "description": "Primary brand color"
    },
    "blue": {
      "500": { "value": "#3b82f6", "type": "color" }
    }
  },
  "spacing": {
    "1": { "value": "4px", "type": "dimension" },
    "2": { "value": "8px", "type": "dimension" }
  }
}
```

This format is consumed by token transformation tools (Style Dictionary, Tokens Studio, or
custom build scripts) that output platform-specific files: CSS custom properties for web,
Swift/Kotlin constants for mobile, XML attributes for Android.

### JavaScript/TypeScript Objects (For JS-first systems)

```typescript
export const tokens = {
  color: {
    primary: { default: '#3b82f6', hover: '#2563eb', active: '#1d4ed8' },
    background: '#f3f4f6',
    text: { primary: '#111827', secondary: '#6b7280' },
  },
  spacing: { 1: '0.25rem', 2: '0.5rem', 4: '1rem', 8: '2rem' },
  fontSize: { sm: '0.875rem', base: '1rem', lg: '1.125rem', xl: '1.25rem' },
  borderRadius: { sm: '0.25rem', md: '0.5rem', lg: '1rem', full: '9999px' },
  shadow: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
} as const
```

This approach works naturally with CSS-in-JS libraries (styled-components, Emotion), Tailwind
config extensions, and React Native StyleSheet definitions.

### SCSS Variables and Maps (For Sass-based projects)

```scss
$color-primary: #3b82f6;
$color-background: #f3f4f6;
$spacing: (1: 0.25rem, 2: 0.5rem, 4: 1rem, 8: 2rem);
$font-size: (sm: 0.875rem, base: 1rem, lg: 1.125rem);
```

---

## Multi-Theme Support

The two-tier token structure (reference + semantic) enables theming. To support multiple themes
(light, dark, high contrast, brand variants), keep the reference palette constant and create
alternate semantic mappings.

```css
/* Light theme (default) */
:root {
  --color-background: var(--color-white);
  --color-text-primary: var(--color-gray-900);
  --color-surface: var(--color-gray-50);
}

/* Dark theme */
[data-theme="dark"] {
  --color-background: var(--color-gray-900);
  --color-text-primary: var(--color-gray-50);
  --color-surface: var(--color-gray-800);
}
```

Because atoms reference semantic tokens (`--color-background`, not `--color-white`), every atom
automatically adapts to the active theme with zero code changes. This is one of the most powerful
benefits of the token layer.

For multi-brand support (same product, different visual identities), create brand-specific
reference palettes that feed into the same semantic token structure:

```css
[data-brand="acme"] { --color-blue-500: #0066cc; }
[data-brand="widget-co"] { --color-blue-500: #0099ff; }
```

---

## How Tokens Connect to Atoms

Every visual property in an atom must reference a token. Hard-coded values in atoms are a code smell
that indicates a missing token.

```tsx
// WRONG — hard-coded values in the atom
const Button = styled.button`
  background: #3b82f6;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
`;

// CORRECT — all values from tokens
const Button = styled.button`
  background: var(--color-primary);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
`;
```

If you find yourself needing a value that no token provides, add a new token — do not add a
hard-coded value. The token set should grow to cover all legitimate visual needs.

---

## Token Governance

As the system grows, tokens need governance to prevent bloat and inconsistency.

Tokens should be added through a review process. Before adding a new token, verify that no
existing token serves the same purpose. Naming should follow the established convention exactly.
Every token should have a description explaining its intended use.

Deprecated tokens should be marked and removed in phases — first add a deprecation notice, then
after a migration period, remove the token and update all references.

Token values should be audited periodically against the actual usage in components. Unused tokens
add cognitive overhead without value and should be pruned.

---

## Token Extraction During Refactoring

When refactoring an existing codebase (see `refactoring-playbook.md`), token extraction is one of
the first steps. The process:

1. Scan all source files for hard-coded color values (hex, rgb, hsl), font sizes, spacing values,
   border radii, shadows, and z-index values.
2. Group identical and near-identical values (e.g., `#333` and `#343434` are likely the same token).
3. Name each group using the token naming convention.
4. Create the token file in the appropriate format for the project.
5. Update atoms to reference tokens. Do not update higher levels directly — they should inherit
   token usage through their atom and molecule dependencies.
6. Verify visual output has not changed after the switch from hard-coded values to tokens.
