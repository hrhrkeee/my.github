# Create React Native environment template

Create or update the repository environment template for a **React Native** project.

Work in this order:

1. Read `.github/copilot-instructions.md` if it exists.
2. Read all files under `project/environment/` if they exist.
3. Inspect the repository for environment markers before making assumptions:
   - `package.json`, lock files, workspace files, monorepo config files
   - `app.json`, `app.config.*`, `metro.config.*`, `babel.config.*`, `tsconfig*.json`
   - `android/`, `ios/`, `Podfile`, Gradle files, fastlane files
   - `.node-version`, `.nvmrc`, `.tool-versions`, `volta` config
   - `Dockerfile*`, `.devcontainer/*`, `.github/workflows/*`
   - `jest.config.*`, `detox`, `maestro`, `eslint*`, `prettier*`
4. If critical information is missing or ambiguous, ask precise questions before finalizing the template.
5. Prefer a template that is explicit about Node, package manager, React Native toolchain, Android/iOS requirements, and emulator/device workflows.

Create or update these files as appropriate:

- `project/environment/environment.yaml`
- `project/environment/detected-environment.md`
- `project/environment/command-matrix.md`
- `project/environment/compatibility-matrix.md`
- optionally, the nearest environment-related runbook under `docs/runbooks/`

## Requirements for `project/environment/environment.yaml`

Populate it as the authoritative environment definition for this repository.
Use YAML and include at least these keys:

```yaml
project_name:
project_type: react-native
summary:
default_branch:
node:
  version:
  version_file:
package_manager:
  primary:
  lock_files: []
  install_commands: []
typescript:
  enabled:
react_native:
  version:
  architecture:
  engine:
toolchain:
  xcode:
  cocoapods:
  android_studio:
  jdk:
  gradle:
  ruby:
execution_context:
  os:
  supported_platforms: []
  emulator_profiles: []
repository_layout:
  app_dirs: []
  shared_package_dirs: []
  test_dirs: []
  config_dirs: []
  native_dirs: []
commands:
  setup: []
  install_js: []
  install_ios: []
  start_metro: []
  run_android: []
  run_ios: []
  test: []
  lint: []
  format: []
  typecheck: []
  e2e: []
  build_debug: []
  build_release: []
quality_gates:
  minimum_local_checks: []
  slower_checks: []
external_dependencies:
  services: []
  secrets: []
  signing: []
ci:
  workflow_files: []
  parity_notes:
notes:
  assumptions: []
  open_questions: []
```

## Domain-specific expectations

The template must explicitly cover these React Native concerns when applicable:

- Node and package manager pinning
- iOS and Android native toolchain requirements
- Metro, Babel, and TypeScript integration
- New Architecture / Hermes / Fabric / TurboModules status if detectable
- monorepo or workspace boundaries if present
- simulator / emulator / physical device workflows
- JS unit tests vs end-to-end test strategy
- CocoaPods and Gradle installation/update expectations
- environment variable and secret handling
- build/debug/release command separation
- local development vs CI differences

## Rules

- Do not invent Expo usage, bare workflow usage, or New Architecture status without repository evidence.
- If both Expo and bare React Native signals exist, call out the ambiguity and ask targeted questions.
- If iOS tooling cannot be validated from the current machine or repo, mark it as an open question rather than fabricating versions.
- If Android signing or release automation is absent, state that clearly.
- If the repo is a monorepo, identify the app package and the shared package boundaries.
- Keep `detected-environment.md` descriptive and evidence-based.
- Keep `compatibility-matrix.md` focused on versions, supported platforms, and development host assumptions.
- Keep `command-matrix.md` actionable and copy/paste-friendly.

## Output expectations

Return:

- the files created or updated
- key assumptions
- unanswered questions that block full accuracy
- the recommended local setup flow for macOS and, if relevant, Windows
- the minimal validation commands to run after the template is accepted
