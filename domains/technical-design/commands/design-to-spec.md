Translate a design description into a technical specification.

Take the user's design description (visual, interaction, UX, or feature description) and produce a structured technical spec using the spec-translator methodology.

Process:
1. Extract the design intent — what is the designer trying to achieve?
2. Map subjective terms to concrete engineering values using the bridging vocabulary (domains/technical-design/prompts/bridging-vocabulary.md)
3. Identify all states (loading, error, empty, overflow — not just happy path)
4. Note technical constraints relevant to implementation
5. List open questions that need design clarification

Output a spec with these sections:
- **Design Intent**: 2-3 sentences in the designer's language
- **Behavior**: Concrete terms with states and transitions
- **Qualitative Targets**: Table mapping design goals to engineering targets
- **States**: Table of state name, trigger, and behavior
- **Constraints**: Platform/performance/accessibility boundaries
- **Open Questions**: Specific questions that need answers before implementation

Every subjective design term must be translated to a measurable value. Every spec must preserve the original design intent.

$ARGUMENTS
