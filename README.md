# Awesome Product Building — Cursor Rules

Canonical Cursor rule books for shipping products with AI coding agents. Install or symlink `.cursor/rules/` into a project (or copy the lean set you need).

## The 8 rule books

| Book | File | When it applies |
|------|------|-----------------|
| **Agent Ops** | `agent-ops.mdc` | Always (`alwaysApply: true`). Ask-first edits, research workflow, git sync before merge/push, clean code. |
| **Create Web App / Game** | `create-web-game.mdc` | Web/HTML/CSS/JS(X) apps & browser games — SPA/static ship, hosting, engine/shell, embeds, PWA. |
| **Convert Web → Mobile** | `convert-web-to-mobile.mdc` | Android WebView/Capacitor shells, Gradle, themes, mobile UX, pre-ship checks. |
| **Publish Mobile** | `publish-mobile.mdc` | Signed AAB, Play listing honesty, Console upload, ASO, phased rollout. |
| **Product Excellence** | `product-excellence.mdc` | Stack-agnostic philosophy, multi-device UI/a11y, security, privacy, Definition of Done. |
| **System Design** | `system-design.mdc` | HLD/LLD — problem framing, NFRs, diagrams, traceability, design-done criteria. |
| **Incubation** | `incubation.mdc` | Ultrathink UI, vision/idea tables, pattern wedges, 10-step gate, CIRCLES critique. |
| **SEO & GTM** | `seo-gtm.mdc` | Product marketing context, brand/copy, on-page & programmatic SEO, site-wide audit. |

## Recommended installs

| Surface | Books |
|---------|--------|
| **Full canonical** (this repo / marketing+product sites) | All 8 |
| **Lean game/product repos** (e.g. Bharat Brawlers) | `agent-ops`, `create-web-game`, `convert-web-to-mobile`, `publish-mobile`, `product-excellence`, `system-design` |
| **Home (`~/.cursor/rules`)** | `agent-ops` (+ local plugins index); personas archived separately |
| **Org monorepo (`Documents/git`)** | `agent-ops` + domain books (`deliverability`, `scala-stack`) |

## Layout

```
.cursor/rules/
  agent-ops.mdc
  create-web-game.mdc
  convert-web-to-mobile.mdc
  publish-mobile.mdc
  product-excellence.mdc
  system-design.mdc
  incubation.mdc
  seo-gtm.mdc
  _archive/          # superseded single-purpose rules (kept for history)
```

## Cross-refs (intent ownership)

- Implementation discipline → `agent-ops.mdc`
- Web/game ship mechanics → `create-web-game.mdc`
- Android packaging/shell → `convert-web-to-mobile.mdc`
- Store release → `publish-mobile.mdc`
- UI/security/DoD → `product-excellence.mdc`
- Architecture before code → `system-design.mdc`
- Ideation & critique → `incubation.mdc`
- Positioning & SEO → `seo-gtm.mdc`

## Symlinks

Projects may symlink `.cursor/rules` to this canonical directory. Do not replace a working symlink with a copied tree unless you intentionally want a divergent local set.

## License / use

Personal/team Cursor rules. Copy or symlink as needed; keep this repo as the source of truth for the eight books.
