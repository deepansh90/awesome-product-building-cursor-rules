---
name: mobile-app-product-ui
description: Build or refine mobile app UI for iOS, Android, React Native, and Flutter with platform conventions, safe-area correctness, touch ergonomics, and accessibility.
disable-model-invocation: true
---

# Mobile App Product UI

Use this skill for mobile-first interface work.

## Inputs to collect

- Platform target (`SwiftUI`, `Jetpack Compose`, `React Native`, `Flutter`)
- Primary user task per screen
- Navigation pattern (tabs, stack, modal, drawer)
- Device constraints (phone-only vs phone+tablet)

## Workflow

1. Choose platform interaction baseline:
   - iOS Human Interface style expectations,
   - Material-style Android expectations,
   - or adaptive cross-platform behavior.
2. Define semantic tokens and state variants.
3. Implement core screens with safe-area and keyboard handling.
4. Add loading/error/empty/disabled states.
5. Validate orientation, dynamic text sizing, and reduced motion.

## Non-negotiable checks

- Touch targets: >=44pt iOS, >=48dp Android.
- Readable contrast in both light and dark modes.
- Back navigation and deep links are predictable.
- Forms use clear labels and in-context errors.
- No critical action is gesture-only.

## Output style

- Keep per-screen purpose singular and clear.
- Prefer native primitives and semantics over custom gestures.
- Keep animations meaningful and interruptible.
