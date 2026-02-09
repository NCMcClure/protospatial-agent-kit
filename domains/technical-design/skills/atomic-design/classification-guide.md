# Component Classification Guide

This reference provides a systematic decision framework for classifying UI components into
the five atomic levels. Use it whenever classification is ambiguous — especially at the
molecule-vs-organism boundary, which is the most common source of team debate.

## The Decision Tree

Work through these questions in order for any component you need to classify.

### Question 1: Is it an irreducible UI primitive?

Can this component be broken into smaller meaningful UI parts? If splitting it would produce
fragments that have no standalone UI purpose (e.g., splitting a button into "button background"
and "button text" makes no sense), then it is an **atom**.

Atoms are the fundamental HTML elements (or their framework equivalents) plus abstract design
properties. They have no dependencies on other components — only on design tokens.

**Examples of atoms:** Button, TextInput, Label, Heading, Paragraph, Icon, Avatar, Image, Badge,
Divider, Spinner/Loader, Checkbox, RadioButton, Toggle/Switch, Slider, Tag/Chip, Link, Textarea.

**Edge case — compound native elements:** An HTML `<select>` element contains `<option>` children,
but it functions as a single native control. Treat it as an atom. Similarly, a radio group where
the radios are always used together and have no independent meaning should be a single atom.

### Question 2: Does it combine a small number of atoms into a single-purpose unit?

If the component groups 2–4 atoms that work together to accomplish one specific micro-task, and
that grouping is reusable in multiple contexts, it is a **molecule**.

The key test: does the molecule have a single responsibility? A search field (label + input +
button) has one job: accept a search query. A form field (label + input + error text) has one
job: capture and validate a single piece of data. If you can describe the molecule's purpose in
one short sentence without using "and," it is likely a well-scoped molecule.

**Examples of molecules:** SearchField (label + input + button), FormField (label + input +
validation message), NavItem (icon + text + link), MediaObject (thumbnail + text block),
StatCard (icon + number + label), Breadcrumb (chain of link atoms + separator atoms),
DropdownTrigger (button + chevron icon), DatePickerInput (input + calendar icon + label).

### Question 3: Does it form a recognizable section of a user interface?

If the component creates a distinct, standalone region of the UI that a non-technical stakeholder
would recognize and name (e.g., "the header," "the sidebar," "the product listing"), it is an
**organism**.

Organisms have contextual identity — they are "the header of this website" or "the comment thread
under the article." They may contain molecules, atoms, and even other organisms. They define what
data they need but do not fetch it.

**Examples of organisms:** SiteHeader (logo + navigation + search + user menu), Footer (links +
copyright + social icons), ProductCard (image + title + price + rating + add-to-cart), HeroSection
(background + headline + subtitle + CTA button), CommentThread (list of comment cards + reply form),
NavigationBar (logo + nav items + user avatar), Sidebar (navigation + filters + branding), PricingTable
(rows of feature comparisons + CTA per tier), DataTable (header row + data rows + pagination + sort
controls), LoginForm (heading + email field + password field + submit + forgot password link).

### Question 4: Is it a page-level layout skeleton?

If the component arranges organisms into a spatial page structure and contains only placeholder
content (no real data, no business logic), it is a **template**.

Templates look like wireframes expressed in code. They define grid areas, column layouts, sidebar
widths, content regions, and responsive breakpoints. They say "the header goes here, the main content
goes here, the sidebar goes here" without saying what the header contains.

**Examples of templates:** DashboardTemplate (header slot + sidebar slot + main content area + footer
slot), ArticleTemplate (header + hero area + two-column body + related articles slot + footer),
AuthTemplate (centered card on a full-bleed background), SettingsTemplate (sidebar nav + tabbed content
area), LandingPageTemplate (hero + feature sections + testimonials + CTA + footer).

### Question 5: Is it a template filled with real content?

If it is a specific instantiation of a template with actual data, real images, real text, and real
user interactions wired up, it is a **page**.

**Examples:** HomePage, ProductDetailPage, UserProfilePage, CheckoutPage, BlogPostPage, SettingsPage.

---

## The Molecule vs. Organism Boundary

This is the most contentious classification decision. Here are five heuristics that resolve most
ambiguities.

**Heuristic 1 — The "Could a stakeholder name it?" test.** Show the component to a non-technical
person. Would they give it a name like "the header" or "the product card"? If yes, it is an organism.
If they would need a developer to explain what it is, it is probably a molecule.

**Heuristic 2 — The single-responsibility test.** Can you describe the component's purpose in one
sentence without the word "and"? If yes, it is likely a molecule. If its purpose requires "and" to
describe ("it shows the logo AND the navigation AND the search bar"), it is an organism.

**Heuristic 3 — The reusability test.** Is this component used in many different organisms? Then it
is a molecule. Is it a self-contained section used in templates/pages? Then it is an organism.

**Heuristic 4 — The complexity test.** Does the component contain only atoms? It is likely a molecule.
Does it contain molecules and/or other organisms? It is an organism.

**Heuristic 5 — When in doubt, go higher.** If a component genuinely straddles the boundary, classify
it as an organism. It is safer to have a simple organism than an over-complex molecule. You can always
decompose later.

---

## Worked Examples

### Example 1: Is a navigation bar a molecule or an organism?

A navigation bar typically contains a logo (atom), several nav items (molecules: icon + text + link),
and possibly a search field (molecule) and user menu (molecule). It forms a recognizable interface
section that a stakeholder would call "the nav bar." It composes multiple molecules. **Classification:
organism.**

However, a *single nav item* (icon + label) is a molecule — it groups two atoms for one purpose.

### Example 2: Is a product card a molecule or an organism?

A product card contains an image (atom), heading (atom), price (atom), rating stars (molecule), and
an add-to-cart button (atom). It forms a recognizable unit a stakeholder would identify. It combines
both atoms and at least one molecule. **Classification: organism.**

However, if the card is extremely simple — just an image and a title with no interactive elements —
it could be argued as a molecule. Apply heuristic 5: classify it as an organism and move on.

### Example 3: Where do forms go?

Forms are often organisms. A login form (email field molecule + password field molecule + submit
button atom + forgot-password link atom) is a recognizable interface section. A registration form
with many fields is even more clearly an organism.

However, a single form field (label + input + error message) is a molecule — it serves one purpose
and groups a few atoms. The form *organism* composes multiple form field *molecules*.

### Example 4: Is a modal a molecule or an organism?

A modal overlay typically contains a title (atom), body content (variable — could be molecules or
organisms), action buttons (atoms), and a close button (atom). It manages focus trapping and
backdrop interactions. It is a recognizable interface pattern. **Classification: organism.**

If the modal's inner content is itself complex (e.g., a multi-step wizard), the inner content may
contain its own organisms. The modal container remains an organism that wraps other organisms.

### Example 5: Is a tooltip a molecule or an atom?

A tooltip trigger (the element you hover) is an atom. The tooltip content itself (a floating text
box) is also an atom — it is a single UI primitive that displays text. The combination of trigger +
positioned content + arrow could be considered a molecule, but most frameworks treat the tooltip as
a single unified component. **Pragmatic classification: atom.** The positioning logic is an
implementation detail, not a composition of meaningful sub-components.

### Example 6: Is a dropdown/select a molecule or an organism?

A simple dropdown (button + floating list of options) is a **molecule** — it does one thing (lets the
user pick from a list) and combines a few atom-level elements. A complex multi-select with search
filtering, grouping, create-new functionality, and tag display starts to feel like an organism due
to its internal complexity. Apply the single-responsibility test: if describing it requires "and," it
has grown into an organism.

---

## Common Misclassifications to Avoid

**Wrapping every HTML element in an atom.** Not every `<div>` or `<span>` needs to be an atom. Atoms
are *meaningful* UI primitives. A layout wrapper div is not an atom — it is a structural implementation
detail.

**Making molecules too complex.** If a molecule has more than 4–5 atom children or contains another
molecule, it has likely outgrown the molecule level. Promote it to an organism.

**Putting business logic in organisms.** Organisms define data contracts (the shape of data they
accept) but must not contain API calls, global state mutations, or routing logic. That belongs in pages.

**Treating templates as organisms.** A template is not just a big organism — it is a fundamentally
different abstraction. Templates define page-level spatial layout. If it does not define where
*sections* of a page go, it is not a template.

**Classifying utility components.** Layout utilities (Container, Grid, Stack, Flex), animation
wrappers, and error boundaries are infrastructure, not atoms. Place them in a separate `utils/` or
`layouts/` directory outside the atomic hierarchy. They support the system but are not part of the
atomic classification.
