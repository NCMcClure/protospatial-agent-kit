# Prototype Fidelity Ladder

A framework for choosing the right prototype level. Each level validates different questions at different costs.

## The Five Levels

### Level 1: Paper
**Form**: Sketches, storyboards, flow diagrams, sticky notes
**Tools**: Whiteboard, paper, Miro, FigJam
**Time**: Minutes to hours
**Validates**: Concept viability, user flow logic, information architecture, stakeholder alignment on direction
**Cannot Validate**: Spatial feel, interaction timing, technical feasibility, performance
**Stop here when**: The question is "should we build this?" or "does this flow make sense?"
**Move up when**: Flow is agreed upon and you need to validate the *feel* of the interaction

### Level 2: Wireframe
**Form**: Static layouts, spatial diagrams, component inventories
**Tools**: Figma, Sketch, hand-drawn with dimensions
**Time**: Hours to a day
**Validates**: Layout structure, spatial relationships, information hierarchy, component inventory, rough sizing
**Cannot Validate**: Interaction feel, animation timing, real-world scale (in XR), technical constraints
**Stop here when**: The question is "what goes where?" or "what information does this surface show?"
**Move up when**: Layout is settled and you need to validate interaction patterns

### Level 3: Interactive
**Form**: Clickable/tappable prototype, basic state transitions, simulated interactions
**Tools**: Figma prototyping, HTML/CSS/JS, engine graybox with placeholder interaction
**Time**: Days
**Validates**: Navigation patterns, interaction sequences, basic usability, state transitions, rough timing
**Cannot Validate**: Performance, real data behavior, edge cases, production visual fidelity, XR comfort at scale
**Stop here when**: The question is "does this interaction pattern work?" or "can users figure this out?"
**Move up when**: Interaction pattern is validated and you need to prove technical feasibility or tune feel

### Level 4: Functional
**Form**: Real logic with representative data, running in target platform (or close proxy)
**Tools**: UE5 graybox with C++, standalone app prototype, engine with placeholder art
**Time**: Days to a week
**Validates**: Technical feasibility, interaction feel with real input, performance characteristics, data-driven edge cases, XR comfort
**Cannot Validate**: Final visual quality, full content coverage, production art pipeline
**Stop here when**: The question is "can we build this?" or "does this feel right with real input?"
**Move up when**: Feasibility is proven and you're moving toward shippable quality

### Level 5: Polished
**Form**: Production visuals, real data, full state coverage, accessibility
**Tools**: Full engine implementation, production art, QA testing
**Time**: Weeks
**Validates**: The complete experience — does it ship?
**Cannot Validate**: Nothing at this level is hypothetical. This IS the product.
**Stop here when**: This is the release.

## Decision Framework

```
What question are you trying to answer?

"Should we build this?"
  → Paper (Level 1)

"What goes where? What's the structure?"
  → Wireframe (Level 2)

"Does this interaction pattern work?"
  → Interactive (Level 3)

"Can we build this? Does it feel right?"
  → Functional (Level 4)

"Is it ready to ship?"
  → Polished (Level 5)
```

## Fidelity Mistakes

### Over-investing Early
Building a polished prototype to test a concept. If the concept is wrong, all the polish is wasted. Test the concept with paper, then invest in polish only after the concept is validated.

### Under-investing at Crunch Time
Using a wireframe to evaluate interaction feel. Wireframes can't communicate timing, weight, or responsiveness. If the question is about how something *feels*, you need at least Level 3 (Interactive).

### Mixing Fidelity Signals
A prototype with polished visuals but broken interactions sends mixed signals. Stakeholders will focus on the visuals and give visual feedback instead of the interaction feedback you need. Match fidelity across dimensions.

### Skipping Levels
Going from Paper directly to Functional. Each level validates something the previous level cannot. Skipping levels means you're building on unvalidated assumptions.

## XR-Specific Considerations

- **Spatial scale can only be validated in-headset.** A Figma mockup at "arm's reach" is a guess. Even graybox in-engine viewed on a monitor is a guess. XR interactions need at least Level 3 in-headset to validate spatial relationships.
- **Comfort requires real frame rates.** A 30fps prototype cannot validate that an interaction is comfortable at 90Hz. Performance is a comfort feature in XR.
- **Hand tracking needs real hands.** Simulated input (mouse/keyboard pretending to be hands) cannot validate hand tracking interactions. Use the real input device at Level 3+.
