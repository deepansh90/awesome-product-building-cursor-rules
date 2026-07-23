---
name: game-tester
description: >-
  Bharat Brawlers / Ranbhoomi game fleet tester: pull latest code, ui-ux-pro-max
  search bootstrap, multi-persona UI/gameplay audit (mobile, game design, UX),
  live playtest ≥10 minutes across games, unit/e2e regression, rebuild DSA embeds
  + Android web, then push main and fast-forward master on Ranbhoomi + dsapatterns.
  Use when the user asks for game-tester, regression ship, playtest, fleet UI
  audit, or regenerate DSA/Android games.
---

# game-tester

**Upstream:** `/Users/deepanshrawal/Documents/git/Bharat Brawlers` (`deepansh90/Ranbhoomi`)  
**Host vendor:** `/Users/deepanshrawal/Documents/git/dsapatterns-website` (`deepansh90/dsapatterns.io`)  
**Rules:** `/Users/deepanshrawal/Documents/git/awesome-product-building-cursor-rules`

Stop on first hard failure (tests / build). Never force-push. Never `--no-verify`.

Modes (user may ask for one or all):

| Mode | What |
|------|------|
| `audit` | Pro Max search + multi-persona review + live playtest (no push required) |
| `ship` | Sync → tests → embeds → android web → commit → push main/master |
| `full` | `audit` then ranked quick wins gate → `ship` |

Default when user says "run game-tester": **`full`**.

## Paths

```bash
RANBHOOMI="/Users/deepanshrawal/Documents/git/Bharat Brawlers"
DSA="/Users/deepanshrawal/Documents/git/dsapatterns-website"
RULES="/Users/deepanshrawal/Documents/git/awesome-product-building-cursor-rules"
UIUX_PRO_MAX="/Users/deepanshrawal/Documents/git/ui-ux-pro-max-skill"
SEARCH_PY="$UIUX_PRO_MAX/src/ui-ux-pro-max/scripts/search.py"
```

```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export ANDROID_SDK_ROOT="$HOME/Library/Android/sdk"
```

BB vendored `ui-ux-pro-max` is checklist-only (no CSV/scripts). **Always** run `python3 "$SEARCH_PY"` from `$UIUX_PRO_MAX`.

---

## Checklist

```text
- [ ] 0. Fetch latest on RANBHOOMI + DSA (+ RULES if editing skill)
- [ ] 0.5 Pro Max search bootstrap (catalog evidence for personas)
- [ ] 1. Multi-persona audit (parallel subagents)
- [ ] 1.5 Quick wins gate (full / "fix quick wins")
- [ ] 2. Live playtest ≥10 minutes, ≥8 games
- [ ] 3. npm test (+ optional e2e)
- [ ] 4. Rebuild DSA embeds + vendor
- [ ] 5. Android --web --all
- [ ] 6. Commit if shipping
- [ ] 7. Push main then ff master
- [ ] 8. Report (Pro Max + personas + quick wins + playtest + SHAs)
```

---

## 0. Take latest code

```bash
cd "$RANBHOOMI" && git fetch origin && git checkout main && git pull --ff-only origin main
cd "$DSA" && git fetch origin && git checkout main && git pull --ff-only origin main
```

If dirty: stash/commit first. Never discard remote with reset/`--ours`.

---

## 0.5 Pro Max search bootstrap (mandatory before §1)

Run once; paste top hits into every persona prompt. Domains: `ux`, `web`, `product`, `style`, `icons`, `gsap`.

```bash
python3 "$SEARCH_PY" "casual puzzle game mobile" --design-system -p "Ranbhoomi"
python3 "$SEARCH_PY" "touch accessibility contrast safe-area" --domain ux
python3 "$SEARCH_PY" "safe areas touch hitSlop" --domain web
python3 "$SEARCH_PY" "play pause settings home undo" --domain icons
python3 "$SEARCH_PY" "press feedback reduced-motion" --domain gsap
```

Persona prompts **must cite** search hits + `file:line`. Do not claim Pro Max review without this step.

---

## 1. Multi-persona audit (parallel)

Launch **3+ subagents** with isolated prompts. Ground each in RULES + Pro Max hits from §0.5:

| Persona | Rules / skill | Games (split catalog) | Must check |
|---------|---------------|------------------------|------------|
| **Mobile Optimizer** | `convert-web-to-mobile.mdc`, embed-game-ui.css + Pro Max touch/web | Patchwork, ArrowRush, Grid TD, Equalize | Safe-area; **≥44×44** hit (`min-h/min-w`, not padding alone); **≥8px** gaps; no hover-only; no `w-6`/`h-6` icon-only chrome; dock vs fragmented chrome; Undo border when disabled; check **embed CSS cascade** (`dsapatterns-*-embed.css` + game `embed-game-ui.css`), not only Tailwind `min-h`/`min-w` |
| **Game Designer** | `create-web-game.mdc`, incubation / Jobs HUD | Equalize, TimeTwin, Helicopter, Sanctum/Orbit | Minimal HUD; first-session teach; fail/win juice; pacing; max **1–2** key motions that don't block input |
| **UI/UX Critic** | `product-excellence.mdc` Rams + Pro Max Quick Ref | Train Panic, Optic, Tank Wars, Circuit, Crush | Contrast **4.5:1**; icon-only `aria-label`; `prefers-reduced-motion`; bottom nav **≤5**; predictable back + modal dismiss; Lucide/Heroicons (no emoji chrome); style clash vs Equalize dock |
| **SEO / Hub** (optional) | `seo-gtm.mdc` | embed-registry + GAME_BRIEF | displayName parity; levelCount truth; **iframePath / hub iframeSrc = lobby roots only** (`/games/<slug>/`) — never `/play`, `/campaign`, `/rush/*` |

### Pro Max → fleet chrome (UI/UX Critic + Mobile)

| Dimension | Fleet check |
|-----------|-------------|
| **Touch** | ≥44×44; ≥8px gap; tap not hover-only; expand hit beyond tiny SVG |
| **A11y** | 4.5:1 contrast; icon-only `aria-label`; respect `prefers-reduced-motion` |
| **Motion** | 150–300ms micro; ≤1–2 hero motions; never block Undo/tap |
| **Nav** | Bottom ≤5; predictable back; modal dismiss/escape |
| **Icons** | No emoji as Undo/Theme/Mute; consistent stroke; Lucide/Heroicons language |
| **Product map** | Casual Puzzle / Arcade / Word → style hints Clay, Pixel, HUD/Cyberpunk Mobile — **flag clash** vs Equalize dock reference |
| **Pre-delivery** | 375px smoke + one landscape pass on a canvas game; Dynamic Type large if text HUD |

Prior fleet findings (re-check when relevant):

- **External walkthroughs** (Gemini/Antigravity/etc.): re-validate every item against **current HEAD** before implementing — most are often already fixed
- **Embed CSS overrides touch:** measure computed size with `dsapatterns-*-embed.css` + game `embed-game-ui.css` together — rem caps (`2rem`/`2.5rem`) can beat source 44px (Crush)
- **ThemeSwitcher false P0:** do not flag "needs 44px" if shared `.btn-theme-switcher` already has min ≥ `2.75rem` — verify computed size
- Patchwork Undo: never `disabled:border-transparent` — keep chip stroke
- Equalize footer = **reference** dock (Home · Sound · Undo · Reset · Theme) — **reference ≠ require** an identical 5-button bar on every title; fleet default remains BR Theme+Audio chips, migrate toward Equalize over time
- Fleet BR theme/vol pill vs in-board actions = unify over time
- Sanctum nested routes (`/campaign`): SPA fallback smoke — DSA `serve.json` and/or CF/Vercel rewrite; plain `npx serve` without SPA = 404 P0
- **Hub iframe deep links load DSA cheat sheet in-frame (P0):** hub `iframeSrc` / registry `iframePath` must be **lobby roots only** (`/games/<slug>/`). Never `/play`, `/campaign`, `/rush/*` in the hub iframe — on dsapatterns.io those paths are not static files and CF/SPA fallthrough serves the **parent DSA SPA** inside the game iframe. Cross-repo: DSA `GamesSection` iframeSrc must match Ranbhoomi `EMBED_GAMES` iframePath lobby contract. Playtest must open hub `#games/<slug>`, assert iframe `src` is lobby root **and** iframe document is the game shell (title/body contains game brand), not DSA cheat-sheet chrome

Each persona returns **P0/P1/P2** with `file:line` (+ search cite). Incomplete agents (1–2 lines, no severity) → **re-run**. Parent synthesizes; prefer a Cursor Canvas for the aggregated report.

---

## 1.5 Quick wins gate (`full` / "fix quick wins")

After §1, parent emits a **ranked** quick-wins list (each ≤ ~30 min) before ship when `mode=full`.

| Priority | Typical |
|----------|---------|
| P0 | Touch <44, missing `aria-label`, contrast fails, hover-only primary |
| P1 | 8px gaps, emoji chrome icons, disabled Undo ghost border, reduced-motion |
| P2 | Style clash, dock unify, dense Tailwind cleanup |

If user said **"fix quick wins"**: implement **P0/P1 touch/a11y first**, then continue playtest/ship. Otherwise list in report and proceed unless user stops for fixes.

---

## 2. Live playtest (≥10 minutes)

Prefer a real browser (Playwright or browser MCP). If browser tools fail, fall back to **deep static analysis** of assigned game React/HTML under `$RANBHOOMI/games/` — still emit P0/P1/P2 with `file:line`.

Serve options:

```bash
# Vendored embeds (DSA public) — recommended for ship verification
cd "$DSA" && npx --yes serve public -l 4177
# Dev hub (if Vite already running): http://localhost:5173/games/<slug>/
```

Requirements:

- Wall clock **≥ 10 minutes** of interaction across games
- Visit **≥ 8** slugs (rotate): equalize, patchwork, arrow-rush, grid-tower-defense, time-twin, crush-the-cups, train-panic, circuit-flow, optic-beam-puzzle, helicopter-rush, tank-wars
- Per visit: dismiss tutorial → poke board/canvas → try Undo/Hint/Reset → Theme/Mute if present → screenshot
- Record: dock present? theme btn count? audio btn count? undo border/disabled ghost? pageerrors? deep-link 404s?
- **Hub iframe contract:** for each visited slug, open hub `#games/<slug>`, assert iframe `src` is lobby root (`/games/<slug>/` or `equalize.html`) **and** iframe document is game shell (title/body contains game brand) — not DSA cheat-sheet chrome
- Deep-link at least one nested SPA route (e.g. `/games/grid-tower-defense/campaign`) when using `serve` **directly** — **not** as hub `iframeSrc` (hub stays lobby roots); expect SPA fallback not 404

**Pro Max playtest add-ons:**

- [ ] Icon-only controls have accessible name (hover/devtools or SR)
- [ ] Adjacent chrome gaps ≥8px (spot-check dock)
- [ ] `prefers-reduced-motion` smoke if easy (OS/DevTools)
- [ ] Landscape once for **one** canvas game (ArrowRush / Helicopter / Tank)

Do not claim playtest without duration + game list.

---

## 3. Regression tests

```bash
cd "$RANBHOOMI"
npm test
# optional:
npm run test:e2e:android-regression
```

---

## 4–5. Regenerate DSA + Android

```bash
cd "$RANBHOOMI"
node scripts/games/build-all-embeds.mjs
node scripts/games/android/run.mjs --all --web
```

Pin `docs/upstream-sync/bharat-brawlers/VENDOR-MANIFEST.json` → `ranbhoomiSha` = `git rev-parse HEAD`.

---

## 6–7. Commit + push (ship / full only)

```bash
# Ranbhoomi (if dirty)
cd "$RANBHOOMI"
git add -A && git status   # no secrets
git commit -m "$(cat <<'EOF'
chore(ship): game-tester pass — embeds, android web, tests green

EOF
)"
git fetch origin && git push origin main && git push origin main:master

# DSA
cd "$DSA"
git add public/games docs/upstream-sync/bharat-brawlers/VENDOR-MANIFEST.json public/sitemap.xml
git commit -m "$(cat <<'EOF'
chore(games): vendor Ranbhoomi after game-tester

EOF
)"
git fetch origin && git push origin main && git push origin main:master
```

**RULES repo:** push `main` only (no `main:master` unless a `master` branch exists and is documented).

Non-ff `main:master` → stop; no `--force` unless user asks.

---

## 8. Report template

```markdown
## game-tester report
### Sync
- Ranbhoomi / DSA tips after pull

### Pro Max
- Queries run: design-system + ux + web + icons + gsap
- Top hits: (1–3 bullets each domain — style/product cues for fleet)

### Personas (P0/P1/P2 bullets + file:line)
- Mobile Optimizer: …
- Game Designer: …
- UI/UX Critic: …

### Quick wins (ranked, ≤30min each)
1. P0 …
2. P1 …
3. …

### Playtest
- Duration: Xm · Games: … · Crashes: 0/N
- Pro Max: reduced-motion / icon labels / 8px gaps / landscape: yes/no/skip
- Chrome bugs: Undo ghost / missing dock / contrast / …

### Ship
- Tests: pass/fail
- Embeds / Android web: ok
- Ranbhoomi `<sha>` · DSA `<sha>` · pushed main+master: yes/no
```

---

## Anti-patterns

```text
❌ Claiming Pro Max review without running search.py (BB skill has no CSV)
❌ Audit-only praise without P0 file:line evidence
❌ Incomplete persona agents (1–2 lines) — require P0/P1/P2 + file:line or re-run
❌ Emoji as Undo/Theme/Mute/Settings chrome icons
❌ Hover-only affordances on mobile embeds
❌ Claim 10 min playtest without wall-clock log
❌ Push without fetch / ff-only pull
❌ Vendor DSA from stale Ranbhoomi
❌ Force-push main/master
❌ Skip 44–48px check on canvas-overlay HTML controls
❌ Strip borders on disabled Undo/Hint (looks "broken")
❌ Re-implementing walkthrough items without re-checking HEAD
❌ Auditing Tailwind touch mins while ignoring embed CSS rem overrides
❌ Flagging ThemeSwitcher 44px when shared embed-game-ui already sets 2.75rem
❌ Hub iframeSrc / registry iframePath with `/play`, `/campaign`, or `/rush/*` (CF/static fallthrough → parent DSA SPA in frame)
❌ Playtest that only hits `/games/<slug>/` directly and never asserts hub `#games/<slug>` iframe src + in-frame game brand
```

## Related

- **ui-ux-pro-max (upstream + search):** `$UIUX_PRO_MAX` · `SEARCH_PY` — BB mirror checklist only: `$RANBHOOMI/.cursor/skills/ui-ux-pro-max/SKILL.md`
- `webapp-to-android` · `convert-web-to-mobile.mdc` · `create-web-game.mdc` · `product-excellence.mdc` · `seo-gtm.mdc`
- Embed: `build-all-embeds.mjs` · `vendor-dsapatterns.mjs`
- Git hygiene: `agent-ops.mdc`
