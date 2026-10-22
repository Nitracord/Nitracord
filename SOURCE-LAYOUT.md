# Source layout

The main repository owns the project root and `tools/`. Each component below is an independent Git checkout.

```text
.github/
  profile/README.md Organization overview
  assets/           Profile branding, icons and badges

nitracord-patcher-core/
  src/main/java/app/nitracord/patcher/core/
    apk/          Normalization, manifest/resources, signing and runtime config
    bundle/       Bundle schema, immutable rule data, HTTPS update/cache protocol
    compat/       Structural compatibility inspection
    dex/          Generic DEX edits, React hooks and identity rewriting
  src/test/java/  Bundle/cache and generated-DEX regression checks
  build.gradle    Pinned Maven dependencies
  licenses/
  gradle/         Wrapper and Java formatter shared with frontends

nitracord-patches/
  patches/manifest.json    Privacy targets, fingerprints, actions, diagnostics, baselines
  bundles/default.ncp     Generated offline and OTA payload
  index.json              Generated OTA version, URL and bundle hash
  runtime/src/main/java/app/nitracord/runtime/
    diagnostics/          Bounded startup log
    plugins/              Plugin API and metadata
    themes/               Theme parsing, colors and persistence
    ui/                   Settings, restart and system insets
  runtime/src/main/smali/app/nitracord/runtime/HookProvider.smali
  runtime/src/main/assets/ JavaScript runtime and offline font
  runtime/prebuilt/        Compiled native client payload
  tests/                  JavaScript regressions
  tools/                  Native payload and deterministic bundle builders

nitracord-patcher-cli/
  src/main/java/app/nitracord/cli/Main.java

nitracord-patcher-app/
  app/src/main/java/app/nitracord/patcher/
    apk/          Archive inspection
    provider/     Read-only APK sharing
    signing/      Android Keystore identity
    ui/           Patcher and patch update UI
  app/src/main/res/
  app/src/main/jniLibs/

nitracord-plugins/
  src/            Importable JavaScript plugins
  docs/
  examples/
  tests/
  tools/

nitracord-themes/
  themes/         Importable theme JSON
  examples/
  tools/
```

Both patchers use `app.nitracord:nitracord-patcher-core:0.0.1`, substituted with the independent local checkout. Each frontend supplies the appropriate ARSCLib platform distribution. The Android runtime is compiled separately with the Android SDK.

Client assets use `assets/nitracord/`, plugin metadata uses `NitracordPlugin`, and settings use `nitracord://settings` (package-scoped for alongside installs).
