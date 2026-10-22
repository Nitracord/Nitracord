# Source maintenance

Use JDK 17+ and Node 18+. Nitracord release versions are **0.0.1** across the core, patchers, bundles, runtime, plugins and themes. Android versionCode is **1**. Dependency and schema/API versions are independent.

## Java

In core, CLI, app or patches, run:

```sh
./gradlew formatJava
./gradlew checkJavaFormat
```

Windows uses `gradlew.bat`. Google Java Format 1.24.0 formats sources/imports. Frontends use `nitracord-patcher-core/gradle/java-format.gradle`; override with `-PcoreDir`. Patches have their own formatter so runtime development does not need a core checkout.

## JavaScript and JSON

In patches, plugins or themes:

```sh
npm ci
npm run format
npm run format:check
npm test
```

Prettier 3.4.2 is pinned in lockfiles. Generated catalogs, hashes and bundles are excluded. After plugin/theme edits, run `node tools/build-catalog.mjs`.

After runtime Java/smali edits, run `node tools/build-hook.mjs /path/android.jar /path/build-tools/lib/d8.jar` in patches. This rebuilds DEX and asset hashes. Then run `python tools/build-bundle.py` to regenerate the bundle/index. Recipe-only edits need only the bundle rebuild.

## Checks

| Checkout       | Command                                                        |
| -------------- | -------------------------------------------------------------- |
| Core           | `gradlew.bat build checkJavaFormat`                            |
| Patches        | `gradlew.bat build checkJavaFormat` and `npm run format:check` |
| CLI            | `gradlew.bat build installDist checkJavaFormat`                |
| App            | `gradlew.bat :app:assembleDebug checkJavaFormat`               |
| Plugins/themes | `npm test` and `npm run format:check`                          |

Core checks read the sibling patches bundle by default; use `-PpatchesDir=/path/to/patches` elsewhere. They cover updates, invalid-download cache preservation, engine compatibility, integrity and bundle-controlled DEX edits/exclusions.

Run `python tools/export-source.py` from the main root to export sources. Keep keys, SDK paths, node_modules and outputs out of source commits/exports. Preserve applicable copyright and license notices when reorganizing files.
