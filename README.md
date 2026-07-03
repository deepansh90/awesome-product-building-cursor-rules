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
| [`website-building.mdc`](.cursor/rules/website-building.mdc) | Web Applications (Static & SPA) | Sites, SPA deploy, dsapatterns.io map (§ DSA Patterns), vendored bundles |
| [`automation-software.mdc`](.cursor/rules/automation-software.mdc) | Browser & Form Automation | Selenium/Playwright bots |
| [`games-building.mdc`](.cursor/rules/games-building.mdc) | Game Development | Engine, embed, host iframe hardening (§12), PWA, TanStack CSR suite |
| [`web-to-android-app-conversion.mdc`](.cursor/rules/web-to-android-app-conversion.mdc) | Web-to-Android | WebView/Capacitor shells, Play icons/screenshots, §13 listing audit, §14 TanStack pipeline, **§15 Studio + Play publish** |
| [`cursor-agent-discipline.mdc`](.cursor/rules/cursor-agent-discipline.mdc) | Agent Discipline | How AI edits code (always on) |
| [`agent-discipline.mdc`](.cursor/rules/agent-discipline.mdc) | Agent Discipline (minimal) | Ask-first, minimal-change behavior (always on) |
| [`java-spring-end-to-end.mdc`](.cursor/rules/java-spring-end-to-end.mdc) | Java Spring End-to-End | Spring Boot + JPA + test pyramid |
| [`product-council.mdc`](.cursor/rules/product-council.mdc) | Product Council (CIRCLES) | Idea/spec critique before build |
| [`steve-jobs.mdc`](.cursor/rules/steve-jobs.mdc) | Steve Jobs & Mindful Essentialist | Ultrathink UI (no feature changes); vision Q&A; idea tables; essentialism |
| [`on-page-seo.mdc`](.cursor/rules/on-page-seo.mdc) | On-Page SEO | Titles, content, internal links, page audits |
| [`product-marketing-context.mdc`](.cursor/rules/product-marketing-context.mdc) | Product Marketing Context | Shared ICP, positioning, voice (`.agents/product-marketing.md`) |
| [`brand-strategy.mdc`](.cursor/rules/brand-strategy.mdc) | Brand Strategy | Positioning, values, segmentation, tone, creative direction |
| [`marketing-copy.mdc`](.cursor/rules/marketing-copy.mdc) | Marketing Copy | Headlines, CTAs, landing/home/pricing page copy |
| [`seo-audit.mdc`](.cursor/rules/seo-audit.mdc) | SEO Audit | Site-wide crawlability, technical SEO, ranking diagnosis |
| [`programmatic-seo.mdc`](.cursor/rules/programmatic-seo.mdc) | Programmatic SEO | Scaled template pages, directories, pSEO playbooks |

**Optional archive** (not in default `.cursor/rules/` copy): drafts under [`.cursor/Don't include these/`](.cursor/Don't%20include%20these/) — e.g. `python-web-backend.mdc`, `apple-mobile-swiftui.mdc`, `ai-seo.mdc`, `off-page-seo.mdc`, `google-ads.mdc`, `github-workflows.mdc`. Cherry-pick into your project if needed.

## Cherry-pick by product type

| Product type | Recommended rules |
|--------------|-------------------|
| Any product | `universal-product`, `cursor-agent-discipline` |
| New idea, PRD, or major bet | + `steve-jobs` Mode B/C for ideation or vision Q&A → then `product-council` → `system-design` |
| UI polish pass (no new features) | + `steve-jobs` Mode A (with `universal-product`) |
| Feature overload / scope cut | + `steve-jobs` Mode C essentialism probes or `product-council` **Cut** step |
| New feature / architecture | + `system-design` |
| Web app (React/Vite/etc.) | + `website-building` |
| Python API / form bot | + `python-web-backend` from archive; + `automation-software` if browser-driven |
| Java / Spring full stack | + `java-spring-end-to-end` |
| iOS / SwiftUI | + `apple-mobile-swiftui` from archive |
| Game (browser, embed, PWA) | + `product-council` + `games-building` |
| Game embedded in parent site | + `games-building` + `website-building` |
| Web game → Google Play (WebView or Capacitor) | + `web-to-android-app-conversion` + `games-building` |
| New brand or rebrand | + `product-marketing-context` → `brand-strategy` → `marketing-copy` |
| Marketing / growth (SEO, AI search, Google Ads) | + `on-page-seo`; + `seo-audit` for troubleshooting; + `programmatic-seo` for scaled landings; + `off-page-seo`, `ai-seo`, `google-ads` from archive if needed |
| SEO troubleshooting (traffic drop, not ranking) | + `seo-audit` → then `on-page-seo` for page fixes |
| Scaled SEO landing pages (templates + data) | + `programmatic-seo` + `on-page-seo` + `website-building` |

## Tool boundaries

- **UI generators** — layout, components, visual iteration.
- **IDE agents** — auth, database, payments, tests, CI, hardening.

Keep both in sync via Git. See [Lovable + Cursor workflow](https://github.com/murataslan1/cursor-ai-tips/blob/main/tips/lovable-cursor-workflow.md).

## Attributions

Patterns informed by community collections and public best-practice guides, including:

- [cursor-ai-tips](https://github.com/murataslan1/cursor-ai-tips) (agent workflow, common mistakes)
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) (Conventional Commits, Playwright E2E, Python/Java/SwiftUI stack patterns)
- [marketingskills](https://github.com/coreyhaines31/marketingskills) (product-marketing, copywriting, seo-audit, marketing-psychology patterns)
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (programmatic SEO playbooks, brand-guidelines)
- [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) (programmatic SEO quality control at scale)

- **Dieter Rams** — product/UI principles referenced in `universal-product.mdc` §1b (clarity, honesty, as little design as possible)
- **CIRCLES** — product sense framework (Lewis C. Lin); used in `product-council.mdc`
- **Steve Jobs / Mindful Essentialist** — ultrathink design and essentialism; used in `steve-jobs.mdc`

## License

MIT — see [LICENSE](LICENSE).
