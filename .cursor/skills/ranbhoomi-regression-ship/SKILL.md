---
name: ranbhoomi-regression-ship
description: >-
  Regression ship for Ranbhoomi (Bharat Brawlers) game fleet: pull latest,
  run unit/e2e regression tests, rebuild DSA embeds, regenerate Android web
  assets, commit if needed, and push main then fast-forward master on
  Ranbhoomi + dsapatterns-website. Use when the user asks for regression
  testing, ship verification, regenerate DSA/Android games, or push
  main/master after game UI changes.
---

# Ranbhoomi regression ship

**Upstream:** `/Users/deepanshrawal/Documents/git/Bharat Brawlers` (remote `deepansh90/Ranbhoomi`)  
**Host vendor:** `/Users/deepanshrawal/Documents/git/dsapatterns-website` (remote `deepansh90/dsapatterns.io`)  
**Rules skill repo (this skill):** `/Users/deepanshrawal/Documents/git/awesome-product-building-cursor-rules`

Stop on first failure. Never force-push. Never `--no-verify`. Never amend unless the user asks.

## Checklist (copy and tick)

```text
- [ ] 1. Sync latest on all repos
- [ ] 2. Unit / game regression tests (Ranbhoomi)
- [ ] 3. Rebuild all DSA embeds + vendor
- [ ] 4. Regenerate Android web assets (--web --all)
- [ ] 5. Optional: Android e2e regression specs
- [ ] 6. Commit Ranbhoomi if dirty (ask if unclear; proceed when user said "ship" / "execute skill")
- [ ] 7. Commit DSA vendor if dirty
- [ ] 8. Push main then ff master (both game repos)
- [ ] 9. Report SHAs + commands run
```

## Paths

```bash
RANBHOOMI="/Users/deepanshrawal/Documents/git/Bharat Brawlers"
DSA="/Users/deepanshrawal/Documents/git/dsapatterns-website"
RULES="/Users/deepanshrawal/Documents/git/awesome-product-building-cursor-rules"
```

Export when Android Gradle is involved:

```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
export ANDROID_SDK_ROOT="$HOME/Library/Android/sdk"
```

---

## 1. Take latest code

On **each** of `$RANBHOOMI` and `$DSA`:

```bash
git fetch origin
git checkout main
# Prefer stash/commit WIP before pull if dirty
git pull --ff-only origin main
git log HEAD..origin/main --oneline   # must be empty
```

If local WIP blocks pull: stash or commit first — never discard remote with reset/`--ours`.

Also fetch `$RULES` if committing the skill itself.

---

## 2. Regression tests (Ranbhoomi)

```bash
cd "$RANBHOOMI"
npm test
# Focused game unit suite (when only games changed):
node --test tests/games/*.test.mjs
```

Optional Playwright (slower; run when user asks for full e2e or after embed UI changes):

```bash
npm run test:e2e:android-regression
# Full embed e2e (rebuilds embeds first):
# npm run test:e2e:games
```

Do not claim "tests pass" without command output.

---

## 3. Regenerate DSA games (embeds + vendor)

```bash
cd "$RANBHOOMI"
# All embeds → vendors into $DSA/public/games/<slug>
node scripts/games/build-all-embeds.mjs
# Or full vendor helper (install + build + ranbhoomi embed + manifest):
# npm run vendor:dsapatterns
```

Confirm `$DSA/public/games/` updated and `docs/upstream-sync/bharat-brawlers/VENDOR-MANIFEST.json` has current `ranbhoomiSha`.

Partial rebuild (faster when only a few slugs changed):

```bash
for slug in <slug...>; do node scripts/games/build-all-embeds.mjs "$slug" || exit 1; done
```

---

## 4. Regenerate Android games (web assets)

Default for regression ship: **web only** (CSR into each game's `dist/android-client/`). Skip full Gradle unless user asks for APK/AAB.

```bash
cd "$RANBHOOMI"
node scripts/games/android/run.mjs --all --web
```

Single game:

```bash
node scripts/games/android/run.mjs <slug> --web
```

Full native (patch + web + gradle + icons):

```bash
npm run android:all
```

---

## 5. Commit

**Only when** the user asked to ship / execute this skill / commit, or working tree must be committed to push.

### Ranbhoomi

```bash
cd "$RANBHOOMI"
git status
git add -A   # review: no secrets (.env, keystores)
git commit -m "$(cat <<'EOF'
chore(ship): regression pass — embeds, android web, tests green

EOF
)"
```

### dsapatterns-website

```bash
cd "$DSA"
git add public/games docs/upstream-sync/bharat-brawlers/VENDOR-MANIFEST.json public/sitemap.xml
git commit -m "$(cat <<'EOF'
chore(games): vendor Ranbhoomi embeds after regression ship

EOF
)"
```

Pin `ranbhoomiSha` in the manifest to `git rev-parse HEAD` from Ranbhoomi after the Ranbhoomi commit.

---

## 6. Push main + fast-forward master

Never assume local tip is current — `fetch` again right before push.

```bash
# Ranbhoomi
cd "$RANBHOOMI"
git fetch origin
git push origin main
git push origin main:master

# DSA
cd "$DSA"
git fetch origin
git push origin main
git push origin main:master
```

If `main:master` is non-ff, stop and report — do not `--force` unless the user explicitly requests it.

---

## 7. Report template

```markdown
## Regression ship report
- Ranbhoomi: `<sha>` (main = master)
- DSA: `<sha>` (main = master)
- Tests: `npm test` → pass/fail
- Embeds: build-all-embeds → ok
- Android: run.mjs --all --web → ok
- Pushed: yes/no
- Blockers: none | …
```

---

## Anti-patterns

```text
❌ Push without fetch / pull --ff-only
❌ Vendor DSA from stale Ranbhoomi tip
❌ Claim e2e green without running Playwright
❌ Force-push main/master
❌ Skip android --web when UI changed for Play WebView shells
❌ Edit only public/games/ on DSA without rebuilding upstream
```

## Related

- Android pipeline details → `webapp-to-android` skill / `convert-web-to-mobile.mdc`
- Embed sync → `scripts/games/build-all-embeds.mjs`, `vendor-dsapatterns.mjs`
- Agent git hygiene → `agent-ops.mdc` (take latest before merge/push)
