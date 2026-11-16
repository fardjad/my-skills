---
name: justfile-conventions
description: Apply project conventions when creating, editing, or reviewing justfiles and Just recipes.
---

# Justfile conventions

Name the file `justfile`, in lowercase.

## Recipe organization

- Make `help` the first recipe so the default guidance is visible when listing tasks.
- Implement `help` with `@just --list` so the list remains concise.
- Give each public recipe a short description immediately above it so `just --list` shows its purpose and any important side effects.
- Hide implementation-only helpers from listings with a leading underscore or `[private]`. This is discoverability, not access control.

## Recipe names

- Use lowercase, hyphen-separated names. Prefer a short action or action-plus-scope, such as `build`, `test-unit`, or `format-check`.
- Prefer conventional names such as `build`, `test`, `lint`, `format`, and `clean` when they apply; do not add placeholder recipes.
- If `check` aggregates quality checks, document which checks it runs and do not silently fix source files. Keep explicitly mutating tasks, such as `format`, separate from their checking counterparts.
- Document installation destinations, permissions, and external side effects. Uninstall only what was installed.
- Prefer one clear name per task. Add aliases only when they provide a real benefit.

## Cleanup and maintenance

Add these recipes only when useful. Document what they remove or change; never delete source files, local configuration, secrets, or user data by default. The `clean`, `mostlyclean`, `distclean`, and `maintainer-clean` names follow GNU Make's standard targets.

- `clean`: remove ordinary generated build artifacts.
- `mostlyclean`: leave expensive-to-rebuild artifacts in place when a quicker cleanup is useful.
- `clean-cache`: remove only caches that can be recreated.
- `distclean`: also remove generated configuration, while preserving user-authored configuration.
- `maintainer-clean`: remove additional distributed generated files; warn when rebuilding them requires special tools.
- `doctor`: report missing prerequisites or configuration problems without changing state.
- `update-deps`: make dependency updates explicit, including network access and changes to lockfiles.

## Shell behavior

- Avoid a global `set shell` override. Keep shell selection local to recipes that need it.
- For multi-line shell recipes, use a recipe-level Bash shebang and enable strict mode with `set -euo pipefail`.
- Use a different interpreter only when the recipe specifically requires it, and keep its behavior explicit.
- Keep simple single-command recipes as simple commands instead of adding unnecessary shell wrappers.

## Environment variables

- When recipes need dotenv variables, use Just's native loading: `set dotenv-load` for `.env`, or `dotenv-filename` / `dotenv-path` for a specific variant or location. Loaded variables are environment variables, not Just variables.
- Keep each dotenv file's adjacent example authoritative, naming it by appending `.example` (for example, `.env.local.example`). Do not inspect, print, or expose real dotenv contents. Pass secrets through the environment rather than interpolating them into recipe text.

## Recipe design

- Use recipes as readable task entry points that delegate to project scripts or standard tools.
- Declare dependencies for real prerequisites or intentional aggregate tasks. Recipes with the same arguments run only once per Just invocation; they are not Make file targets and are not automatically skipped because output files are up to date.
- Quote paths and arguments where needed. For user-supplied arguments interpolated into a Bourne-style shell, use Just's `quote()` function, such as `{{quote(arg)}}`; plain interpolation does not escape shell metacharacters.
- Do not hide destructive behavior. Name and document recipes so their effects are clear.
