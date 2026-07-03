---
name: webapp-to-android
description: >-
  Convert Bharat Brawlers TanStack games to offline Play Store WebView APKs/AABs.
  Use for scaffolding android/, ANDROID_STANDALONE builds, Gradle release bundles,
  Play screenshots, theme/BGM parity, and §13 listing audits.
---

# WebApp to Android — Bharat Brawlers

Canonical rule: `awesome-product-building-cursor-rules/.cursor/rules/web-to-android-app-conversion.mdc` §14–§15.

**One command:**

```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
node scripts/games/android/run.mjs <slug|--all> [--scaffold] [--patch] [--web] [--gradle] [--icons] [--screenshots] [--smoke]
```

Default steps (no flags): `--patch --web --gradle --icons`.

Registry: `scripts/games/android/registry.mjs` (14 games; Equalize excluded).

---

## §0 Architectural and philosophical pillars

### 1. Steve Jobs ultrathink and UI essentialism (`steve-jobs.mdc`)

- **Ruthless HUD economy:** Every control earns its place on mobile. Prefer icons over redundant labels.
- **Frictionless loops:** Replace multi-step game-over dialogs with instant ≤0.5s restart.
- **Visual rhythm and high contrast:** Calm typography across all five themes.

### 2. Game engineering and juice (`games-building.mdc`)

- **Universal 5-theme engine:** `balance`, `ember`, `zen`, `midnight`, `ocean` via `useGameTheme` + `ThemeSwitcher` in `__root.tsx`.
- **Audio and music:** `music-asset-manifest.json` — file loops or procedural BGM; `unlockGameAudio()` on first gesture.
- **Haptic tactility:** `puzzleJuice.ts` / `navigator.vibrate()` on placements, impacts, victories.

### 3. Web and SPA resilience (`website-building.mdc`)

- **Strict build isolation:** Play ships `dist/android-client/` only — never embed `dist/client`.
- **SPA fallbacks:** `SpaAssetsPathHandler.kt` — empty path and extension-less routes → `index.html`.

### 4. Play Store honesty (`product-marketing-context.mdc`, conversion rule §13)

- **120-second discoverability:** Every screenshot bullet must be reachable offline on cold launch.
- **Exact store assets:** 512×512 PNG icon (15% safe zone), real 1080×2400 gameplay screenshots.

---

## §1 Module map (`scripts/games/android/`)

| Script | Purpose |
|--------|---------|
| `run.mjs` | Orchestrator |
| `registry.mjs` | Slugs, packageIds, activity layout |
| `patch-web.mjs` | vite / router / gameBack / `__root` |
| `apply-theme-parity.mjs` | ThemeSwitcher + cycling `useGameTheme` |
| `scaffold.mjs` | Gradle + Kotlin WebView shell |
| `build-web.mjs` | `dist/android-client/` CSR bundle |
| `build-native.mjs` | debug APK, release APK, AAB |
| `fix-icons.mjs` | Launcher mipmaps |
| `screenshot-scenes.mjs` | Per-game Playwright scenes |
| `capture-screenshots.mjs` | 1080×2400 PNG output |
| `audit-parity.mjs` | Report → `docs/android/parity-audit.md` |

---

## §2 New game checklist

1. Add entry to `registry.mjs`
2. `node scripts/games/android/run.mjs <slug> --scaffold --patch`
3. `node scripts/games/android/run.mjs <slug> --web --gradle`
4. `node scripts/games/android/capture-screenshots.mjs <slug>`
5. Fill `docs/play-listings/<slug>.md` (§13 matrix)
6. §15: signed AAB + 120s offline audit before Play upload

---

## §3 Gradle asset sync (production pattern)

```kotlin
val gameWebRoot = layout.projectDirectory.dir("../../dist/android-client")
val syncedGameAssets = layout.buildDirectory.dir("generated/gameAssets")

val syncGameWebAssets by tasks.registering(Sync::class) {
    from(gameWebRoot)
    into(syncedGameAssets)
}

android {
    sourceSets {
        getByName("main") {
            assets.srcDir(syncedGameAssets)
        }
    }
}

tasks.named("preBuild").configure { dependsOn(syncGameWebAssets) }
```

**Not** separate `debug`/`release` sourceSets (AGP 8.13 empty APK trap).

---

## §4 SpaAssetsPathHandler (empty path fix)

```kotlin
override fun handle(path: String): WebResourceResponse? {
    val assetPath = when {
        path.isEmpty() || path == "/" -> "index.html"
        path.startsWith("/") -> path.removePrefix("/")
        else -> path
    }
    assetsHandler.handle(assetPath)?.let { return it }
    val leaf = assetPath.substringAfterLast('/')
    if (!leaf.contains('.') || leaf.startsWith('.')) {
        return assetsHandler.handle("index.html")
    }
    return null
}
```

`game_url` = `https://appassets.androidplatform.net/assets/` (trailing slash).

---

## §5 Critical pitfalls

| Mistake | Fix |
|---------|-----|
| Ship embed bundle to Play | `ANDROID_STANDALONE=1` → `dist/android-client` |
| `basepath` → `./assets/` after patch | Restore `basepath:"/assets/"` in patch-client |
| Wrong Gradle sync path | `../../dist/android-client` from `app/` module |
| Claim themes on Play without UI | ThemeSwitcher visible on home within 120s |
| Test keystore on Play | `dummy123` is local only — production keystore per app |
| WebView slow/choppy animation | Missing `<application android:hardwareAccelerated="true">` in manifest |

---

## §5b WebView Native Hardening (Open Source Best Practices)

When scaffolding or modifying Android web shells, enforce these patterns learned from production wrappers (`shiaho777/web-to-app`, `Jipok/website-to-apk`):

1. **Double Back Press Exit (`MainActivity.kt`):**
   Prevent accidental app termination when navigating UI overlays by intercepting back presses on the root screen: require two back taps within 2000ms along with a short Toast notice (*"Press back again to exit"*).
2. **External Link & Custom Scheme Interception (`WebViewClient`):**
   Override `shouldOverrideUrlLoading` to intercept non-HTTP schemes (`mailto:`, `market://`, `share://`, social intents). Open them safely via system `Intent(Intent.ACTION_VIEW)` rather than allowing WebView navigation to fail or replace the offline game session.
3. **Unblocked WebGL & Audio Playback (`WebSettings`):**
   Always configure:
   ```kotlin
   settings.apply {
       javaScriptEnabled = true
       domStorageEnabled = true
       databaseEnabled = true
       mediaPlaybackRequiresUserGesture = false
   }
   ```
4. **Hardware Acceleration (`AndroidManifest.xml`):**
   Ensure `<application android:hardwareAccelerated="true" ...>` is explicitly set so HTML5 Canvas and WebGL render at 60 FPS.
5. **Fixed Screen Orientation (`AndroidManifest.xml`):**
   HTML5 puzzle/arcade games designed for portrait layout break if the device rotates into landscape. Lock activity orientation using `android:screenOrientation="portrait"` (or `"sensorPortrait"`).
6. **Edge-to-Edge Display Cutout Mode (`styles.xml` / `MainActivity`):**
   On Android 9+ (API 28+), prevent black letterbox bars around camera notches by enabling cutout layout: `android:windowLayoutInDisplayCutoutMode = shortEdges` or programmatically in onCreate via `window.attributes.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES`.

---

## §6 Verification

```bash
node scripts/games/android/run.mjs --all --skip-emulator
node scripts/games/android/audit-parity.mjs
node scripts/games/android/capture-screenshots.mjs --all
npm run test:e2e:games
```

Release smoke: airplane mode cold launch, back button, no fatal logcat.
