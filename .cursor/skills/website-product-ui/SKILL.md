---
name: website-product-ui
description: Build or improve website UI with consistent design systems, responsive behavior, and accessibility. Use when the user asks for landing pages, marketing sites, dashboards, docs sites, or SPA interface polish.
disable-model-invocation: true
---

# Website Product UI

Use this skill for website and SPA UI work.

For deeper visual-system or brand-personality passes, optional Cursor agents: `@ui-designer`, `@ux-architect`, `@brand-guardian`, `@whimsy-injector` — still obey Rams / simplification rules in `universal-product.mdc` and `website-building.mdc`.

## Inputs to collect

- Product type (SaaS, docs, e-commerce, portfolio, game host, etc.)
- Goal of page (convert, explain, onboard, transact, retain)
- Preferred stack (React/Next/Vue/Astro/plain HTML)
- Visual anchor (`DESIGN.md` style or brand direction)

## Workflow

1. Pick one visual anchor:
   - `awesome-design-md` `DESIGN.md` file for style direction, or
   - existing in-repo design tokens/components.
2. Generate/confirm design system (color, typography, spacing, elevation) before one-off screens.
3. Build layout with one primary CTA per route.
4. Implement responsive and keyboard-safe interactions.
5. Run simplification pass: remove duplicated copy and noisy sections.

## Delight and empty states

- Loading, empty, and error surfaces may carry brand personality (tone, light motion, helpful microcopy).
- Whimsy must serve clarity or reduce friction — never decorative chrome that fails the `website-building.mdc` simplification audit or the user's anti-generic frontend rules.
- Respect `prefers-reduced-motion`; never convey meaning through motion alone.

## Non-negotiable checks

- Contrast and focus visibility are preserved.
- No horizontal scrolling on mobile.
- Touch targets are large enough.
- Loading/empty/error states are explicit.
- SEO essentials exist for public pages (title, description, canonical where relevant).

## Output style

- Use concise component-level changes.
- Reuse existing classes/tokens before introducing new ones.
- Document the chosen design anchor in PR/summary notes.
