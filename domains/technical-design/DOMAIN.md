# Technical Design Domain

## Scope

The bridge between design intent and engineering implementation. This domain covers the translation layer where subjective design goals become concrete technical specifications, and where engineering constraints inform design decisions.

### In Scope
- Translating design descriptions into technical specifications (and vice versa)
- Prototype planning at appropriate fidelity levels
- Design-engineering vocabulary mapping
- Breaking specifications into implementation tasks
- Communicating technical constraints as design parameters
- Design review facilitation from a technical lens
- Agentic and spatial UI/UX design workflows

### Out of Scope
- Visual design (color theory, typography, layout grids)
- User research methodology
- Brand identity and marketing design
- Pure engineering implementation (that's the domain-specific work)

## Key Concepts

### Design Intent
The "why" behind a design decision. A spec that says "animate the panel with a 300ms ease-out" is incomplete without "so it feels responsive but not abrupt when the user grabs it." Design intent is the constraint that determines whether an implementation is correct — not just whether it compiles, but whether it *achieves what was meant*.

### Interaction Affordance
What an element communicates about how it can be used. In spatial computing, affordances aren't just visual — they're volumetric, proximity-based, and multi-modal (visual + haptic + audio). A button that glows when your hand approaches is an affordance. A grab handle with resistance is an affordance.

### Fidelity Ladder
A graduated approach to prototype complexity. Not everything needs to be built at full fidelity to validate a hypothesis. Paper sketches validate concepts. Graybox validates spatial relationships. Interactive prototypes validate interaction feel. Each level answers different questions and costs different amounts.

See `prompts/prototype-fidelity.md` for the full framework.

### Specification as Communication Artifact
A spec is not a contract — it's a communication tool. Its purpose is to ensure the designer and engineer share the same mental model. The best specs include: what it should do (behavior), why it should do it (intent), what it should feel like (qualitative targets mapped to quantitative values), and what it should NOT do (boundaries).

### Design Tokens
The sub-atomic design primitives: spacing values, duration curves, color values, type scales. When tokens are well-defined, "make it feel more spacious" becomes "increase spacing from token-4 to token-6." Tokens bridge the subjective-objective gap.

## Conventions

### Specs Always Include Intent
Every technical specification produced from this domain starts with a "Design Intent" section before any technical details. The intent section uses the designer's language. The technical section translates it.

### Prototypes Are Labeled
Every prototype artifact includes its fidelity level (Paper / Wireframe / Interactive / Functional / Polished) so stakeholders know what they're evaluating and what feedback is appropriate.

### Constraints Are Stated Constructively
Lead with what can be done, then qualify with what cannot. "We can support up to 20 interactive elements at 90Hz; beyond that we'd need to batch or LOD" is more useful than "We can't have more than 20 elements."

### Qualitative-to-Quantitative Mapping
Subjective design descriptions are always mapped to measurable values. See `prompts/bridging-vocabulary.md` for the standard mappings.

## Cross-Domain Connections

- **UE5 C++**: Specs from this domain feed directly into UE5 implementation. The header-architect agent can consume a technical spec to produce class architecture. Editor tooling and Slate/UMG work often starts here.
- **Future domains (XR/Spatial)**: Interaction design for spatial computing is the primary consumer of this domain's spec translation and prototype planning capabilities.
