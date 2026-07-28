# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repo is not application code — it is the canonical source of truth for a set of Cursor AI rule books used to build products (games, web apps, mobile apps) across a family of sibling repos (Ranbhoomi, dsapatterns.io, and downstream "Bharat Brawlers" fleet games). Rules here are meant to be copied or symlinked as `.cursor/rules/` into other real projects. There is no build, lint, or test tooling — `package-lock.json` is an empty stub (`{"packages": {}}`, no `package.json`), and the only executable is a single maintenance script.

## Commands

- `python3 scripts/consolidate-rules.py` — the one piece of tooling in this repo. Reads legacy single-purpose `.mdc` rule files from `.cursor/rules/`, strips YAML frontmatter, cross-references filenames via an internal `xref()` rename table, merges them into the canonical "book" files, then archives the originals into `.cursor/rules/_archive/`.

No build/lint/test commands apply — this is a markdown/rules repository.

## Structure

- `.cursorrules` (root) — 4 short directives, duplicated verbatim as the "Core discipline" section of `.cursor/rules/agent-ops.mdc`: ask don't assume, simplest solution first, don't touch unrelated code, flag uncertainty.
- `.cursor/rules/` — the 8 canonical "books" referenced in README.md, each an `.mdc` file with YAML frontmatter (`description`, `alwaysApply`, optional `globs`):
  - `agent-ops.mdc` (alwaysApply) — agent editing discipline: ask-first edits, prefer partial edits over full rewrites, cite file:line, never claim "tests pass" without running them, Conventional Commits (`type(scope): description`), fetch before merging to a shared branch, never force-push.
  - `create-web-game.mdc`, `convert-web-to-mobile.mdc`, `publish-mobile.mdc`, `product-excellence.mdc`, `system-design.mdc`, `incubation.mdc`, `seo-gtm.mdc`.
  - Three additional `alwaysApply: true` files exist beyond the documented "8 books" and represent rule drift worth keeping in sync with the README: `fleet-session-pitfalls.mdc` (incident lessons from live sessions on Ranbhoomi/DSA/Android), `hub-iframe-lobby-roots.mdc` (hub iframe `src` must be a lobby root, not a deep SPA path, or Cloudflare SPA fallthrough leaks the parent site into the game iframe), `play-store-icon-tools.mdc` (Play Store asset generation spec).
  - `_archive/` — 19 superseded single-purpose rule files kept for history, consolidated into the 8 books by `scripts/consolidate-rules.py`.
- `.cursor/commands/ui-ux-pro-max.md` — a slash-command that dispatches to `create-web-game.mdc` or `convert-web-to-mobile.mdc` depending on product type.
- `.cursor/skills/` — 7 skill directories (`game-tester`, `mobile-app-product-ui`, `website-product-ui`, `game-product-ui`, `ui-ux-pro-max-fast-reco`, `fleet-regenerate-ship`, `webapp-to-android`), each a `SKILL.md` with frontmatter. Several are written for *other* projects (Ranbhoomi, dsapatterns.io/DSA hub, Bharat Brawlers) but staged here as the canonical copy.
- `.cursor/MEMORY-hub-iframe.md` — a standalone pinned-lesson memory doc for the hub-iframe incident, cross-referencing which rule/test/skill enforces it in each downstream repo.

## Working in this repo

- When adding or editing a rule, prefer updating the relevant canonical book in `.cursor/rules/` directly rather than creating new standalone `.mdc` files — new always-on files should be rare and, if added, should also be reflected in README.md's "8 books" listing to avoid drift (see the 3 extra `alwaysApply` files above as an example of drift that has already occurred).
- `README.md` documents recommended install combinations of these rules per target repo type (full canonical, lean game/product, home, org monorepo) — check it before deciding which rules a downstream project actually needs.
- Skills and rules that reference sibling repos by name (Ranbhoomi, dsapatterns.io, Bharat Brawlers) are intentionally cross-repo; keep terminology consistent with those repos' own CLAUDE.md/rule files when editing shared concepts like the hub-iframe-lobby-roots invariant.
