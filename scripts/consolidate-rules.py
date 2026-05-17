#!/usr/bin/env python3
"""Consolidate Cursor rules into 8 books. Run from repo root."""
from pathlib import Path
import re
import shutil

ROOT = Path(".cursor/rules")
ARCHIVE = ROOT / "_archive"
ARCHIVE.mkdir(exist_ok=True)


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---\n", 3)
        if end != -1:
            return text[end + 5 :].lstrip("\n")
    return text


def write(name: str, content: str) -> None:
    (ROOT / name).write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"wrote {name} ({len(content.splitlines())} lines)")


def xref(text: str) -> str:
    pairs = [
        ("website-building.mdc", "create-web-game.mdc"),
        ("games-building.mdc", "create-web-game.mdc"),
        ("web-to-android-app-conversion.mdc", "convert-web-to-mobile.mdc"),
        ("mobile-app-building.mdc", "convert-web-to-mobile.mdc"),
        ("universal-product.mdc", "product-excellence.mdc"),
        ("steve-jobs.mdc", "incubation.mdc"),
        ("product-council.mdc", "incubation.mdc"),
        ("startup-incubation-framework.mdc", "incubation.mdc"),
        ("cursor-agent-discipline.mdc", "agent-ops.mdc"),
        ("agent-discipline.mdc", "agent-ops.mdc"),
        ("git-sync-before-merge.mdc", "agent-ops.mdc"),
        ("product-marketing-context.mdc", "seo-gtm.mdc"),
        ("brand-strategy.mdc", "seo-gtm.mdc"),
        ("marketing-copy.mdc", "seo-gtm.mdc"),
        ("on-page-seo.mdc", "seo-gtm.mdc"),
        ("programmatic-seo.mdc", "seo-gtm.mdc"),
        ("seo-audit.mdc", "seo-gtm.mdc"),
    ]
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def main() -> None:
    agent_ops = """---
description: Agent ops — ask-first edits, research workflow, git sync before merge/push, clean code
alwaysApply: true
---

# Agent Ops

**Intent:** How AI coding agents should edit any repository safely — not what product to build (see domain books).

## Core discipline

Ask, don't assume. If something's unclear, ask before writing a line and no silent guesses about intent, architecture, or requirements.

Simplest solution first and implement the minimum thing that works. No abstractions you didn't request.

Don't touch unrelated code and if a file isn't part of the current task, leave it.

Flag uncertainty explicitly or if you're not confident, say so before proceeding as confidence without certainty causes more damage than admitting a gap.

## CRITICAL edit rules

- Prefer **partial edits** (search-and-replace, targeted patches) over rewriting whole files — preserves git history.
- When a full-file replacement is required, output the **complete** file — never placeholders such as `// ... existing code ...` or `# previous implementation`.
- Do not invent changes beyond what the user requested; preserve unrelated code and structure.
- Verify claims against the codebase; cite `file:line` or command output — never claim "tests pass" without running them. Use `@Files` for 2–3 relevant files instead of bloated `@Codebase` context.
- On multi-file work: prefer **one file per commit** when practical; review each diff before stacking the next.

## Tool boundaries (UI generator + IDE)

| Own in UI generators (Lovable, etc.) | Own in Cursor / IDE |
|--------------------------------------|---------------------|
| Layout, components, styling iterations | Auth, database, payments, webhooks |
| Visual feedback loops | Tests, CI, migrations |
| Marketing pages, dashboards (UI) | Complex business logic, security hardening |

Sync via Git: UI tool pushes layout; IDE pushes logic and tests. Use `product_spec.md` and `tech_spec.md` (or equivalent) before large agent sessions.

**Nearest-product UI:** Before generating screens, name the existing product’s look and feel as the anchor. Follow `product-excellence.mdc` §2d — familiar patterns beat generic templates.

## Research-first workflow

1. **Discover** — map how the target area is used before changing it.
2. **Plan** — list files to touch; get approval on non-trivial refactors.
3. **Execute** — implement the approved plan only.
4. **Audit** — review `git diff` line by line before claiming done.

## Git & session hygiene

- Commit (or stash) before long autonomous agent runs.
- **Conventional Commits:** `type(scope): description` — types `feat|fix|docs|refactor|test|chore|ci|perf|build`; optional body explains *why*; `BREAKING CHANGE:` footer or `feat!` when APIs break.
- **PR body must include:** purpose, implementation notes, tests run (exact commands), rollout/rollback note if relevant, linked issue/ticket.
- Fresh chat after ~20 failed debug turns; paste a 3–4 sentence summary + current error.
- Stick to **one model** per task; switch models in a new chat if needed.
- Set API spend limits; require confirmation for destructive terminal commands when available.

## Git: take latest code before merge

Never merge, rebase, cherry-pick onto a shared branch, or push assuming local `main`/`master` is current. Stale local tips silently overwrite remote work.

### Before merge / rebase / push to a shared branch

1. **Fetch first:** `git fetch origin` (or the active remote).
2. **Integrate latest into your base:**
   - Merging to `main`: `git checkout main && git pull --ff-only origin main` (or rebase your feature onto updated `main`).
   - Updating a feature branch: rebase/merge **from** the updated base — do not force-push over others' commits.
3. **Re-check status:** `git status` and `git log HEAD..origin/<base> --oneline` — if remote is ahead, integrate before continuing.
4. **Resolve conflicts deliberately** — never discard remote changes with `git checkout --theirs/--ours` or reset without stating what you are dropping.

### Before long edit sessions

- If the working tree may be stale vs remote: `git fetch` + note whether `origin/<branch>` is ahead.
- Prefer **stash or commit** local WIP before pulling so a pull cannot clobber uncommitted edits.
- After pull, **re-read files you are about to edit** — do not apply patches written against an older tip.

### Anti-patterns

```text
❌ Edit for 30 minutes, then git push --force to main
❌ git merge feature without git fetch / pull on the target branch
❌ Overwrite local files from an old checkout while origin has newer commits
❌ Assume "up to date" from session start after others may have pushed
```

```text
✅ git fetch origin
✅ git pull --ff-only origin main   # on the merge target
✅ rebase/merge feature onto updated main
✅ push only after local base matches remote (or intentional non-ff with user OK)
```

### Exception

Skip only when the user explicitly says to work offline / ignore remote, or when pushing a brand-new branch with no upstream yet (still `fetch` first when the base branch exists).

## Clean code (any language)

- Named constants over magic numbers.
- Meaningful names; single responsibility per function.
- DRY — one source of truth for shared logic.
- Handle edge cases; consider security on every change.
- Add or update tests for new behaviour at trust boundaries.

## What this rule does not cover

- System design documents → `system-design.mdc`
- Product, UI, security policy → `product-excellence.mdc`
- Create web/game → `create-web-game.mdc`
- Convert / publish mobile → `convert-web-to-mobile.mdc`, `publish-mobile.mdc`
- SEO / go-to-market → `seo-gtm.mdc`
- Ideation / scope → `incubation.mdc`
"""
    write("agent-ops.mdc", agent_ops)

    up = xref(strip_frontmatter(read("universal-product.mdc")))
    native = """

## §2e Native / cross-platform mobile baseline **[applicable if iOS/Android/RN/Flutter]**

- One primary job-to-be-done per screen; sketch nav (tabs, stack, modal, deep links) before pixels.
- Touch targets ≥44pt iOS / ≥48dp Android; respect reduced motion and dynamic type.
- Follow native patterns first (iOS swipe-back; Android system back + top app bar).
- Explicit offline, loading, error, success states; persist critical drafts; prevent duplicate submits.
- Never hardcode secrets; minimize permissions; secure storage for sensitive data.
- Web-to-Android packaging → `convert-web-to-mobile.mdc`. Store upload → `publish-mobile.mdc`.
"""
    if "## What this rule does not cover" in up:
        up = up.replace(
            "## What this rule does not cover",
            native + "\n## What this rule does not cover",
            1,
        )
    else:
        up = up.rstrip() + "\n" + native
    up = up.replace("# Universal Product Excellence\n\n", "", 1)
    write(
        "product-excellence.mdc",
        f"""---
description: Product excellence — philosophy, multi-device UI, security, privacy, Definition of Done (stack-agnostic)
alwaysApply: false
---

# Product Excellence

**Intent:** Stack-agnostic product philosophy, UI/a11y, security, privacy, and ship criteria. Surface-specific ship rules → `create-web-game.mdc`, `convert-web-to-mobile.mdc`, `publish-mobile.mdc`.

{up}
""",
    )

    write("system-design.mdc", xref(read("system-design.mdc")))

    web = xref(strip_frontmatter(read("website-building.mdc")))
    games = xref(strip_frontmatter(read("games-building.mdc")))
    games = games.replace("convert-web-to-mobile.mdc §15", "publish-mobile.mdc")
    write(
        "create-web-game.mdc",
        f"""---
description: Create web apps and games — SPA/static ship, copy economy, hosting, game engine/shell, embeds, PWA, verification
globs: "**/*.{{html,css,jsx,tsx,vue,svelte}}","**/wrangler.jsonc","**/vercel.json","**/public/**","**/games/**","**/src/**","**/style.css","**/index.html"
alwaysApply: false
---

# Create Web App / Game

**Intent:** Ship marketing sites, SPAs, and browser games (including embeds/PWA). Convert to Android → `convert-web-to-mobile.mdc`. Store publish → `publish-mobile.mdc`. UI philosophy → `product-excellence.mdc`. SEO → `seo-gtm.mdc`.

**Tag legend:** **[core]** always consider; **[applicable if …]** skip when irrelevant.

---

# Part A — Web applications (static & SPA)

{web}

---

# Part B — Game development

{games}
""",
    )

    w2a = strip_frontmatter(read("web-to-android-app-conversion.mdc"))
    parts = re.split(r"(?=^## §\d+)", w2a, flags=re.M)
    preamble = parts[0]
    sections = {}
    for p in parts[1:]:
        m = re.match(r"^## §(\d+)", p)
        if m:
            sections[int(m.group(1))] = p

    convert_secs = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14}
    order_in_file = []
    for p in parts[1:]:
        m = re.match(r"^## §(\d+)", p)
        if m and int(m.group(1)) in convert_secs:
            order_in_file.append(int(m.group(1)))

    mobile_body = strip_frontmatter(read("mobile-app-building.mdc"))
    mobile_body = re.split(r"\n## Google Play Console Standards", mobile_body)[0]
    mobile_body = xref(mobile_body)

    convert_body = "\n".join([preamble] + [sections[n] for n in order_in_file])
    convert_body = xref(convert_body)
    convert_body = convert_body.replace("This rule §13", "`publish-mobile.mdc`")
    convert_body = convert_body.replace("This rule §15", "`publish-mobile.mdc`")
    convert_body = re.sub(
        r"# Web-to-Android App Conversion\n",
        "# Convert Web App to Mobile\n",
        convert_body,
        count=1,
    )
    write(
        "convert-web-to-mobile.mdc",
        f"""---
description: Convert web apps/games to Android — WebView/Capacitor shells, Gradle sync, themes, graphics, mobile UX, pre-ship verification
globs: "**/android/**","**/equalize-android/**","capacitor.config.*","**/app/build.gradle*","**/README_ANDROID.md","scripts/games/build-android-standalone.mjs","scripts/games/patch-android-client.mjs","scripts/games/generate-android-index.mjs"
alwaysApply: false
---

{convert_body}

---

## Native / cross-platform product UX (when not a thin WebView)

{mobile_body}

## Related books

| Need | Rule |
|------|------|
| Web/game source product | `create-web-game.mdc` |
| UI/a11y baseline | `product-excellence.mdc` |
| Signed AAB, Play listing, Studio publish, ASO | `publish-mobile.mdc` |
""",
    )

    publish_order = []
    for p in parts[1:]:
        m = re.match(r"^## §(\d+)", p)
        if m and int(m.group(1)) in (8, 13, 15, 16):
            publish_order.append(int(m.group(1)))
    publish_body = xref("\n".join(sections[n] for n in publish_order))

    mobile_full = strip_frontmatter(read("mobile-app-building.mdc"))
    play = ""
    if "## Google Play Console Standards" in mobile_full:
        play = "## Google Play Console Standards\n" + mobile_full.split(
            "## Google Play Console Standards", 1
        )[1]

    rel_text = ""
    if (ROOT / "engineering-mobile-release-engineer.md").exists():
        rel_text = strip_frontmatter(read("engineering-mobile-release-engineer.md"))

    write(
        "publish-mobile.mdc",
        f"""---
description: Publish mobile apps — signed AAB, Play listing honesty, Studio test, Console upload, ASO, phased rollout
globs: "**/android/**","**/PLAYSTORE*.md","**/docs/play-listings/**","**/README_ANDROID.md"
alwaysApply: false
---

# Publish Mobile App

**Intent:** Sign, list, and ship to Google Play (and related store hygiene). Packaging/shell work → `convert-web-to-mobile.mdc`. Game/web product → `create-web-game.mdc`.

{publish_body}

---

{play}

---

## Release engineering checklist (policy)

{rel_text}

## Related books

| Need | Rule |
|------|------|
| WebView/Capacitor conversion pipeline | `convert-web-to-mobile.mdc` |
| Web/game source | `create-web-game.mdc` |
| Listing copy voice | `seo-gtm.mdc` |
""",
    )

    seo_files = [
        ("product-marketing-context.mdc", "Section 1 — Product marketing context"),
        ("brand-strategy.mdc", "Section 2 — Brand strategy"),
        ("marketing-copy.mdc", "Section 3 — Marketing copy"),
        ("on-page-seo.mdc", "Section 4 — On-page SEO"),
        ("programmatic-seo.mdc", "Section 5 — Programmatic SEO"),
        ("seo-audit.mdc", "Section 6 — SEO audit"),
    ]
    seo_parts = []
    for fname, title in seo_files:
        seo_parts.append(f"## {title}\n\n{xref(strip_frontmatter(read(fname)))}")
    write(
        "seo-gtm.mdc",
        f"""---
description: SEO and go-to-market — product marketing context, brand, copy, on-page SEO, programmatic SEO, site-wide audit
globs: "**/.agents/product-marketing.md","**/product-marketing*.md","**/*seo*","**/sitemap*","robots.txt","**/marketing/**","docs/**/*.md","**/*.{{html,jsx,tsx,vue,md}}"
alwaysApply: false
---

# SEO & Go-to-Market

**Intent:** One rulebook for positioning, copy, and SEO. Always read `.agents/product-marketing.md` first when it exists. Web ship mechanics → `create-web-game.mdc`. Ideation → `incubation.mdc`.

**Shared opener:** Do not re-ask ICP/voice if the context doc exists — only fill gaps.

**Audit order:** If traffic/rankings are broken, run **Section 6 (audit)** before title tweaks in Section 4. Schema: do not trust `curl` alone for JS-rendered markup — verify in a browser.

{chr(10).join(seo_parts)}
""",
    )

    jobs = xref(strip_frontmatter(read("steve-jobs.mdc")))
    council = xref(strip_frontmatter(read("product-council.mdc")))
    startup = xref(strip_frontmatter(read("startup-incubation-framework.mdc")))
    write(
        "incubation.mdc",
        f"""---
description: Incubation — ultrathink UI, vision/idea tables, pattern wedges, 10-step gate, CIRCLES critique, essentialism
globs: "**/product_spec.md","**/tech_spec.md","**/roadmap.md","**/ROADMAP.md","**/*prd*.md","**/*PRD*.md","**/*idea*.md","**/*startup*.md","**/*incubation*.md","docs/**/*.md","src/**/*.{{tsx,jsx,vue,css,scss}}"
alwaysApply: false
---

# Incubation & Design Critique

**Intent:** Ideate, essentialize, and stress-test product bets before/during build. Architecture → `system-design.mdc`. Implementation discipline → `agent-ops.mdc`. UI philosophy baseline → `product-excellence.mdc`.

**Single 10-step incubation gate:** Use the gate in Part B (Product Council). Do not maintain a second copy.

---

# Part A — Ultrathink, vision & essentialism (Jobs modes)

{jobs}

---

# Part B — Product council (gate + CIRCLES)

{council}

---

# Part C — Startup incubation library (14 lessons, wedges)

{startup}
""",
    )

    to_archive = [
        "agent-discipline.mdc",
        "cursor-agent-discipline.mdc",
        "git-sync-before-merge.mdc",
        "universal-product.mdc",
        "website-building.mdc",
        "games-building.mdc",
        "web-to-android-app-conversion.mdc",
        "mobile-app-building.mdc",
        "engineering-mobile-app-builder.md",
        "engineering-mobile-release-engineer.md",
        "product-marketing-context.mdc",
        "brand-strategy.mdc",
        "marketing-copy.mdc",
        "on-page-seo.mdc",
        "programmatic-seo.mdc",
        "seo-audit.mdc",
        "steve-jobs.mdc",
        "product-council.mdc",
        "startup-incubation-framework.mdc",
        "deepansh90.github-2.io-master.code-workspace",
    ]
    for name in to_archive:
        src = ROOT / name
        if src.exists():
            dest = ARCHIVE / name
            if dest.exists():
                dest.unlink()
            shutil.move(str(src), str(dest))
            print(f"archived {name}")

    active = sorted(p.name for p in ROOT.iterdir() if p.is_file())
    print("ACTIVE:", active)
    expected = {
        "agent-ops.mdc",
        "create-web-game.mdc",
        "convert-web-to-mobile.mdc",
        "publish-mobile.mdc",
        "seo-gtm.mdc",
        "product-excellence.mdc",
        "incubation.mdc",
        "system-design.mdc",
    }
    assert set(active) == expected, active
    print("OK: 8 active books")


if __name__ == "__main__":
    main()
