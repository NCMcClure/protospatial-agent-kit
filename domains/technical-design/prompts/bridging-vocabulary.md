# Design-Engineering Bridging Vocabulary

A reference mapping subjective design language to concrete engineering values. Use this when translating between design descriptions and technical specifications.

## Motion & Animation

| Design Language | Engineering Translation |
|----------------|----------------------|
| "Feels snappy" | Total duration < 200ms, ease-out curve (cubic-bezier 0.0, 0.0, 0.2, 1.0) |
| "Feels responsive" | Initial feedback within 50ms, completion within 150ms |
| "Feels weighty" | Duration 300-500ms, ease-in-out with overshoot (spring-back 5-15% of travel) |
| "Feels smooth" | 60fps minimum, no frame drops during animation, consistent interpolation |
| "Feels natural" | Physics-based or spring animation, not linear. Variable velocity. |
| "Subtle entrance" | Opacity fade 150-200ms combined with 8-16px translate, ease-out |
| "Dramatic entrance" | Scale from 0.8 + opacity fade, 300-400ms, spring overshoot to 1.02 then settle |
| "Instant" | 0ms transition, state change with no interpolation |
| "Quick feedback" | 50-100ms haptic pulse or visual flash, then decay |
| "Breathing / pulsing" | Sine wave on opacity or scale, 2-4s period, 5-15% amplitude |

## Spacing & Layout

| Design Language | Engineering Translation |
|----------------|----------------------|
| "Breathing room" | Padding/margin at 1.5x-2x the base spacing token |
| "Dense but not cluttered" | Base spacing token (4-8px/units), clear visual hierarchy via weight/size, not space |
| "Spacious" | 2x-3x base spacing token, generous margins |
| "Tight grouping" | 0.5x base spacing token between related items, 2x between groups |
| "Comfortable reading distance" | 0.5-2m in VR for body text, 2-10m for signage/headers |
| "At arm's reach" | 0.4-0.7m from user origin in XR |
| "Personal space" | 0.5-1.2m radius around the user; UI in this zone feels intimate/focused |
| "Room scale" | 2-5m radius; elements placed here feel environmental |

## Interaction

| Design Language | Engineering Translation |
|----------------|----------------------|
| "Intuitive grab" | Collision-volume-based detection, 2-4cm activation radius, haptic confirmation on grasp, visual highlight on proximity |
| "Natural pointing" | Ray-cast from hand/controller with 3-5 degree angular tolerance, cursor snap to nearest target within threshold |
| "Direct manipulation" | 1:1 positional/rotational mapping between input and object, no cursor indirection |
| "Forgiving input" | Generous hit targets (minimum 44px / 2cm in XR), Fitts's law compliant, debounced activation |
| "Precise input" | Zoomed/scaled mode, visual guides, snap-to-grid, undo support |
| "Discoverable" | Idle-state animation or proximity-triggered affordance hint, no instruction needed |
| "Progressively disclosed" | Primary action visible, secondary on hover/proximity, tertiary in overflow |

## Quality & Polish

| Design Language | Engineering Translation |
|----------------|----------------------|
| "Production-ready" | All states handled (empty, loading, error, success, overflow, edge), perf within budget, accessibility complete, no placeholder assets |
| "Prototype quality" | Happy path works, primary states covered, known rough edges documented |
| "MVP" | Core value proposition functional, major flows complete, styling may be default/placeholder |
| "Polished" | Micro-interactions complete, transitions tuned, loading states graceful, error recovery smooth |
| "Janky" | Frame drops, inconsistent timing, visual glitches, input lag > 100ms |
| "Buttery" | Consistent 60/90/120fps (target dependent), no hitches, animations interruptible and reversible |

## Spatial (XR-Specific)

| Design Language | Engineering Translation |
|----------------|----------------------|
| "Comfortable" | No artificial vection, stable reference points, < 20ms motion-to-photon latency, comfort rating 1-2 |
| "Immersive" | Minimal UI chrome, diegetic interaction, spatial audio, environment-matched lighting |
| "Grounded" | World-locked elements, surface-snapped, shadow/occlusion with real environment |
| "Floaty" | Unanchored in space, no surface relationship, no shadow — often a problem, sometimes intentional |
| "Presence" | Consistent scale (1:1 real-world), head-tracked parallax, binaural audio, hand/body representation |
| "Glanceable" | Information readable within 0.5s, appropriate for peripheral vision, no head turn required |

## Severity & Priority

| Design Language | Engineering Translation |
|----------------|----------------------|
| "Blocker" | Cannot ship, must fix. Crashes, data loss, or fundamental experience failure. |
| "High priority" | Significantly degrades experience. Fix before release. |
| "Nice to have" | Improves experience but not required. Backlog candidate. |
| "Aspirational" | Future enhancement. Document the intent, don't implement now. |
| "Tech debt" | Works but will slow future development. Track, schedule remediation. |
