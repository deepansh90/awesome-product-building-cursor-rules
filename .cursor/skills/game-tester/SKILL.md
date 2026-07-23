---
name: game-tester
description: >-
  Bharat Brawlers / Ranbhoomi game fleet tester: pull latest code, multi-persona
  UI/gameplay audit (mobile, game design, UX Pro Max), live playtest ≥10 minutes
  across games, unit/e2e regression, rebuild DSA embeds + Android web, then push
  main and fast-forward master on Ranbhoomi + dsapatterns. Use when the user
  asks for game-tester, regression ship, playtest, fleet UI audit, or regenerate
  DSA/Android games.
---

# game-tester

**Upstream:** `/Users/deepanshrawal/Documents/git/Bharat Brawlers` (`deepansh90/Ranbhoomi`)  
**Host vendor:** `/Users/deepanshrawal/Documents/git/dsapatterns-website` (`deepansh90/dsapatterns.io`)  
**Rules:** `/Users/deepanshrawal/Documents/git/awesome-product-building-cursor-rules`

Stop on first hard failure (tests / build). Never force-push. Never `--no-verify`.

Modes (user may ask for one or all):

| Mode | What |
|------|------|
| `audit` | Multi-persona review + live playtest (no push required) |
| `ship` | Sync → tests → embeds → android web → commit → push main/master |
| `full` | `audit` then `ship` |

Default when user says “run game-tester”: **`full`**.

## Paths

```bash
RANBHOOMI="/Users/deepanshrawal/Documents/git/Bharat Brawlers"
DSA="/Users/deepanshrawal/Documents/git/dsapatterns-website"
RULES="/Users/deepanshrawal/Documents/git/awesome-product-building-cursor-rules"
```

```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export ANDROID_SDK_ROOT="$HOME/Library/Android/sdk"
```

---

## Checklist

```text
- [ ] 0. Fetch latest on RANBHOOMI + DSA (+ RULES if editing skill)
- [ ] 1. Multi-persona audit (parallel subagents)
- [ ] 2. Live playtest ≥10 minutes, ≥8 games
- [ ] 3. npm test (+ optional e2e)
- [ ] 4. Rebuild DSA embeds + vendor
- [ ] 5. Android --web --all
- [ ] 6. Commit if shipping
- [ ] 7. Push main then ff master
- [ ] 8. Report (personas + playtest + SHAs)
```

---

## 0. Take latest code

```bash
cd "$RANBHOOMI" && git fetch origin && git checkout main && git pull --ff-only origin main
cd "$DSA" && git fetch origin && git checkout main && git pull --ff-only origin main
```

If dirty: stash/commit first. Never discard remote with reset/`--ours`.

---

## 1. Multi-persona audit (parallel)

Launch **3+ subagents** with isolated prompts. Ground each in local rules + `ui-ux-pro-max`:

| Persona | Rules / skill | Games (split catalog) | Must check |
|---------|---------------|------------------------|------------|
| **Mobile Optimizer** | `convert-web-to-mobile.mdc`, embed-game-ui.css | Patchwork, ArrowRush, Grid TD, Equalize | Safe-area insets; `min-h/min-w` **44–48px** on every control (not only padding); dock vs fragmented chrome; Undo border when disabled |
| **Game Designer** | `create-web-game.mdc`, `incubation.mdc` / Jobs HUD | Equalize, TimeTwin, Helicopter, Sanctum/Orbit | Minimal HUD; first-session teach; fail/win **juice** (haptics, ghost best run); pacing |
| **UI/UX Critic** | `product-excellence.mdc` Rams, ui-ux-pro-max | Train Panic, Optic, Tank Wars, Circuit, Crush | Contrast AA; tabular-nums on timers; dense Tailwind → shared classes; bottom nav ≤5; consistent icon language |
| **SEO / Hub** (optional) | `seo-gtm.mdc` | embed-registry + GAME_BRIEF | displayName parity; levelCount truth; iframePath = first emotion |

Also fold prior fleet findings when relevant:

- Patchwork Undo: never `disabled:border-transparent` — keep chip stroke
- Equalize footer = reference dock (Home · Sound · Undo · Reset · Theme)
- Fleet BR theme/vol pill vs in-board actions = unify over time
- Sanctum nested routes need SPA fallback smoke

Each persona returns **P0/P1/P2** with `file:line` evidence. Parent synthesizes; prefer a Cursor Canvas for the aggregated report.

---

## 2. Live playtest (≥10 minutes)

Serve DSA public (or Vite preview), then Playwright or browser MCP:

```bash
# example static serve
cd "$DSA" && npx --yes serve public -l 4177
```

Requirements:

- Wall clock **≥ 10 minutes** of interaction across games
- Visit **≥ 8** slugs (rotate): equalize, patchwork, arrow-rush, grid-tower-defense, time-twin, crush-the-cups, train-panic, circuit-flow, optic-beam-puzzle, helicopter-rush, tank-wars
- Per visit: dismiss tutorial → poke board/canvas → try Undo/Hint/Reset → Theme/Mute if present → screenshot
- Record: dock present? theme btn count? audio btn count? undo border/disabled ghost? pageerrors? deep-link 404s?

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

Non-ff `main:master` → stop; no `--force` unless user asks.

---

## 8. Report template

```markdown
## game-tester report
### Sync
- Ranbhoomi / DSA tips after pull

### Personas (P0/P1/P2 bullets)
- Mobile Optimizer: …
- Game Designer: …
- UI/UX Critic: …

### Playtest
- Duration: Xm · Games: … · Crashes: 0/N
- Chrome bugs: Undo ghost / missing dock / contrast / …

### Ship
- Tests: pass/fail
- Embeds / Android web: ok
- Ranbhoomi `<sha>` · DSA `<sha>` · pushed main+master: yes/no
```

---

## Anti-patterns

```text
❌ Audit-only praise without P0 file:line evidence
❌ Claim 10 min playtest without wall-clock log
❌ Push without fetch / ff-only pull
❌ Vendor DSA from stale Ranbhoomi
❌ Force-push main/master
❌ Skip 44–48px check on canvas-overlay HTML controls
❌ Strip borders on disabled Undo/Hint (looks “broken”)
```

## Related

- `webapp-to-android` · `convert-web-to-mobile.mdc` · `create-web-game.mdc` · `product-excellence.mdc` · `seo-gtm.mdc`
- Embed: `build-all-embeds.mjs` · `vendor-dsapatterns.mjs`
- Git hygiene: `agent-ops.mdc`
