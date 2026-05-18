# Awesome Product Building — Cursor Rules

Portable [Cursor](https://cursor.com) project rules for building products on **any stack**, **any screen size**, with **Cursor**, **Lovable**, or similar AI builders.

Product and UI guidance is grounded in **Dieter Rams’ ten principles** (clarity, honesty, as little design as possible) — see `universal-product.mdc` §1b for a digital checklist, including when flat UI beats decorative skeuomorphism.

## Install

```bash
git clone https://github.com/<your-org>/awesome-product-building-cursor-rules.git
cp -r awesome-product-building-cursor-rules/.cursor/rules /path/to/your-project/.cursor/rules
```

Or cherry-pick individual `.mdc` files from [`.cursor/rules/`](.cursor/rules/).

**Lovable:** connect this GitHub repo (or sync after pull). For UI-heavy work, use `universal-product.mdc` (§2a–2d covers multi-device UI and nearest-product familiarity). Use Cursor for backend, tests, and deploy.

## Rule catalog

Each rule has a **title** and **intent** at the top. Only `cursor-agent-discipline.mdc` uses `alwaysApply: true`; others activate by context or globs.

| File | Title | When to use |
|------|--------|-------------|
| [`system-design.mdc`](.cursor/rules/system-design.mdc) | System Design (HLD + LLD) | Architecture before implementation |
| [`universal-product.mdc`](.cursor/rules/universal-product.mdc) | Universal Product Excellence | Philosophy, UI/a11y, security, privacy, ship criteria |
| [`website-building.mdc`](.cursor/rules/website-building.mdc) | Web Applications (Static & SPA) | Sites, SPA deploy, hosting vendored bundles |
| [`automation-software.mdc`](.cursor/rules/automation-software.mdc) | Browser & Form Automation | Selenium/Playwright bots |
| [`games-building.mdc`](.cursor/rules/games-building.mdc) | Game Development | Any genre; engine, embed, PWA |
| [`cursor-agent-discipline.mdc`](.cursor/rules/cursor-agent-discipline.mdc) | Agent Discipline | How AI edits code (always on) |
| [`python-web-backend.mdc`](.cursor/rules/python-web-backend.mdc) | Python Web Backends | FastAPI, Django, Flask |
| [`java-spring-end-to-end.mdc`](.cursor/rules/java-spring-end-to-end.mdc) | Java Spring End-to-End | Spring Boot + JPA + test pyramid |
| [`apple-mobile-swiftui.mdc`](.cursor/rules/apple-mobile-swiftui.mdc) | Apple iOS (SwiftUI) | Native iOS apps |
| [`product-council.mdc`](.cursor/rules/product-council.mdc) | Product Council (CIRCLES) | Idea/spec critique before build |

## Cherry-pick by product type

| Product type | Recommended rules |
|--------------|-------------------|
| Any product | `universal-product`, `cursor-agent-discipline` |
| New idea, PRD, or major bet | + `product-council` (before `system-design`) |
| New feature / architecture | + `system-design` |
| Web app (React/Vite/etc.) | + `website-building` |
| Python API / form bot | + `python-web-backend`; + `automation-software` if browser-driven |
| Java / Spring full stack | + `java-spring-end-to-end` |
| iOS / SwiftUI | + `apple-mobile-swiftui` |
| Game (browser, embed, PWA) | + `product-council` + `games-building` |
| Game embedded in parent site | + `games-building` + `website-building` |

## Tool boundaries

- **UI generators** — layout, components, visual iteration.
- **IDE agents** — auth, database, payments, tests, CI, hardening.

Keep both in sync via Git. See [Lovable + Cursor workflow](https://github.com/murataslan1/cursor-ai-tips/blob/main/tips/lovable-cursor-workflow.md).

## Attributions

Patterns informed by community collections and public best-practice guides, including:

- [cursor-ai-tips](https://github.com/murataslan1/cursor-ai-tips) (agent workflow, common mistakes)
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) (Conventional Commits, Playwright E2E, Python/Java/SwiftUI stack patterns)

- **Dieter Rams** — product/UI principles referenced in `universal-product.mdc` §1b (clarity, honesty, as little design as possible)
- **CIRCLES** — product sense framework (Lewis C. Lin); used in `product-council.mdc`

## License

MIT — see [LICENSE](LICENSE).
