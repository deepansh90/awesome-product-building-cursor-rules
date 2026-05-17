---
name: fleet-regenerate-ship
description: >-
  Regenerate Ranbhoomi DSA embeds + Android web assets, run tests, vendor
  dsapatterns, and push main then fast-forward master on Ranbhoomi + DSA.
  Use when the user asks to regenerate DSA/android games, vendor embeds,
  fleet ship, or push games to all remotes without a full game-tester audit.
---

# Fleet regenerate + ship

**Intent:** Upstream rebuild → test → Android web → vendor DSA → push both repos. Not a playtest/audit (use `game-tester` for that).

## Paths

| Role | Default path |
|------|----------------|
| Ranbhoomi | `/Users/deepanshrawal/Documents/git/Bharat Brawlers` |
| DSA | `/Users/deepanshrawal/Documents/git/dsapatterns-website` |
| RULES | `/Users/deepanshrawal/Documents/git/awesome-product-building-cursor-rules` |

Env: `JAVA_HOME` (OpenJDK 17), `ANDROID_SDK_ROOT`, `PATH` includes Homebrew.

## Hard constraints

1. Hub `iframeSrc` / `iframePath` = **lobby roots only** (`/games/<slug>/`) — never `/play`, `/campaign`, `/rush/*`
2. Never `--force` push to `main`/`master`; never `--no-verify`
3. Push order: Ranbhoomi `main` → `main:master`, then DSA `main` → `main:master`
4. RULES repo: push `main` only (no `master` ff unless documented)

## Pipeline (run in order)

```bash
export PATH="/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:$PATH"
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export ANDROID_SDK_ROOT="$HOME/Library/Android/sdk"

RANBHOOMI="/Users/deepanshrawal/Documents/git/Bharat Brawlers"
DSA="/Users/deepanshrawal/Documents/git/dsapatterns-website"

# 0. Sync tips
cd "$RANBHOOMI" && git fetch origin && git checkout main && git pull --ff-only origin main
cd "$DSA" && git fetch origin && git checkout main && git pull --ff-only origin main

# 1. Test
cd "$RANBHOOMI" && npm test

# 2. Embeds (vendors into DSA public/games during build for most games)
cd "$RANBHOOMI" && npm run build:embed:games
# equivalent: node scripts/games/build-all-embeds.mjs

# 3. Android web assets (all shells)
cd "$RANBHOOMI" && node scripts/games/android/run.mjs --all --web

# 4. Vendor + pin VENDOR-MANIFEST to Ranbhoomi HEAD
cd "$RANBHOOMI"
DSAPATTERNS_REPO_PATH="$DSA" node scripts/games/vendor-dsapatterns.mjs

# 5. Commit if dirty (user asked to ship / push)
# Ranbhoomi — only if working tree dirty after rebuild
# DSA — vendor script may already commit; ensure tip pushed

# 6. Push both
cd "$RANBHOOMI"
git push origin main && git push origin main:master

cd "$DSA"
git push origin main && git push origin main:master
```

If Ranbhoomi has uncommitted rebuild artifacts after step 3–4, commit first with Conventional Commit, e.g.:

```text
chore(ship): regenerate embeds + android web; vendor DSA
```

Then re-run `vendor-dsapatterns.mjs` so `VENDOR-MANIFEST.json` `ranbhoomiSha` matches the new tip before pushing DSA.

## Optional e2e

```bash
cd "$RANBHOOMI"
npx playwright test -c playwright.games.config.mjs e2e/games/manual-smoke.spec.mjs
# or targeted: e2e/games/arrow-rush.spec.mjs
```

## Verification gates

- [ ] `npm test` fail = 0
- [ ] `build:embed:games` all games ok + Cloudflare verify ok
- [ ] `android --all --web` every game `"web": "ok"`
- [ ] DSA `VENDOR-MANIFEST.json` `ranbhoomiSha` == Ranbhoomi `git rev-parse HEAD`
- [ ] After push: `origin/main` == `origin/master` on Ranbhoomi and DSA

## Related skills (do not duplicate)

| Skill | When |
|-------|------|
| `game-tester` | Full audit + ≥10m playtest + personas, then this ship path |
| `android-standalone` / `webapp-to-android` | APK/AAB / Gradle / Play listing — not web-only regenerate |
| `hub-iframe-lobby-roots` rule | Never deep-link hub iframes |

## Report (short)

```markdown
## fleet-regenerate-ship
- Ranbhoomi: <sha> (main=master)
- DSA: <sha> pin=<ranbhoomiSha>
- Tests: pass/fail
- Embeds / Android web: ok
- Pushed: yes/no
```
