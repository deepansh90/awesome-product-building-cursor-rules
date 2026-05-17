# Memory — DSA hub iframe lobby roots (Jul 2026)

**Pinned lesson for agents and humans.** Also encoded as always-on rule: `.cursor/rules/hub-iframe-lobby-roots.mdc`.

## What happened
Hub iframes used deep SPA paths (`/play`, `/campaign`, `/rush/blitz`). On dsapatterns.io those are not static files, so Cloudflare fallthrough served the **parent website** inside the game iframe (users saw the cheat sheet / site instead of the game).

## Never again
- Hub `iframeSrc` and Ranbhoomi `iframePath` = `/games/<slug>/` only (Equalize: `equalize.html`).
- Do not “fix first emotion” by deep-linking the hub iframe.
- Keep DSA + Ranbhoomi hub tests on the **same** lobby-root contract.
- Playtest must open `#games/<slug>` and assert iframe shows the **game**, not DSA chrome.

## Where enforced
- RULES: `hub-iframe-lobby-roots.mdc` (alwaysApply), `create-web-game.mdc` §12, `agent-ops.mdc`, `game-tester` skill
- Ranbhoomi: `.cursorrules`, `fleet-hub-fixes.test.mjs`, `embed-registry.mjs`
- DSA: `hub-iframe-titles.test.mjs`, `GamesSection.jsx`

## SEO / docs trap
SEO and host docs must **not** say “deep paths OK with rewrites” for **hub** `iframeSrc` / `iframePath`. Rewrites help direct URL smoke only; the hub contract stays lobby roots (`hub-iframe-lobby-roots.mdc`).
