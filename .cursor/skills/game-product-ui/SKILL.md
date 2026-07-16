---
name: game-product-ui
description: Build game UI and shell UX for browser and mobile game experiences with clear game loops, responsive controls, performance-safe animations, and host integration readiness.
disable-model-invocation: true
---

# Game Product UI

Use this skill for game interfaces, game shells, and embedded game UX.

Pair with `games-building.mdc` (especially §1b craft and §5 HUD). For systems design or level pacing, invoke Cursor agents `@game-designer` / `@level-designer` (optional `@narrative-designer`, `@technical-artist`, `@game-audio-engineer`).

## Inputs to collect

- Game type (puzzle, arcade, strategy, simulation, etc.)
- Core loop (start -> play -> feedback -> retry/progress)
- Host context (standalone web, embedded iframe, mobile wrapper)
- Monetization and onboarding constraints

## Workflow

1. Define loop-first UX (time-to-fun in first session); map moment / session / long-term loops per `games-building.mdc` §1b.
2. Design HUD with ruthless control economy (only essential controls visible).
3. Teach new verbs spatially before wall-of-text tutorials when the layout can carry the lesson.
4. Implement clear success/fail feedback and fast retry — every core verb needs visual + state change; add audio when SFX is on.
5. Ensure responsive controls across mouse, keyboard, and touch.
6. Validate embed/mobile shell compatibility (safe area, orientation, back handling).
7. Add purposeful delight only when it improves clarity or retry momentum; respect `prefers-reduced-motion` (see `@whimsy-injector` bounds — never clutter the playfield).

## Non-negotiable checks

- Input latency and animation smoothness are acceptable.
- Restart and pause are obvious and fast.
- Text and controls remain legible on small screens.
- Audio can be enabled with user gesture and has fallback.
- Empty/blocked states never leave players at a dead end.
- Feedback is complete on core verbs (see Workflow step 4).
- Delight does not fight HUD minimalism or reduced-motion preferences.

## Output style

- Prioritize clarity and momentum over decorative UI.
- Keep score/state feedback immediate.
- Reuse shared game theme tokens across screens.
