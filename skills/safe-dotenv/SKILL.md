---
name: safe-dotenv
description: Reduce the risk of exposing dotenv contents while inspecting schemas and synchronizing local files with adjacent examples. Use when creating, updating, syncing, or troubleshooting .env files.
---

# Safe dotenv files

Use this skill for every task involving dotenv files. Never load real dotenv contents into model context. These precautions are best effort; they cannot guarantee that contents will not be exposed.

## Adoption

When adopting this skill, add the following always-on instruction to the project's `AGENTS.md`, creating it if needed. If an equivalent instruction already exists, do not duplicate it. Resolve conflicts with existing instructions before changing them.

> Never read, inspect, print, or place the contents of real `.env` files into model context. This includes all filename variants and nested files. Do not expose their contents in tool output, logs, diffs, or generated context. Applications and deterministic scripts may read them without exposing their contents.

## Protect local environment files

- Never read, inspect, print, copy into prompts, or otherwise place the contents of a real `.env` file into LLM context. This applies to every `.env` filename variant, including `.env.local` and files in nested directories.
- Do not use tools or commands that could expose `.env` values in output, logs, diffs, or generated context. File paths may be listed, but contents must not be displayed.
- Applications and deterministic local scripts may read `.env` files when needed. This is not permission for an LLM to inspect their contents. Prefer the runtime's built-in dotenv loader; use a small script or programmatic reader only when that is simpler.

## Keep adjacent examples authoritative

- Each local dotenv file should have an adjacent example named by appending `.example`: `.env.example` for `.env`, `.env.local.example` for `.env.local`, and so on. The example is the schema: list variable names in the intended order and document each setting in comments. Do not put secret values in it.
- Add new variables to the example first, using `REDACTED` as their value. Run `python3 <skill-directory>/scripts/sync_env.py path/to/.env.example`, replacing `<skill-directory>` with the directory containing `SKILL.md`. You can also pass the adjacent dotenv file. The utility preserves existing values, adds new variables using the example values, removes variables absent from the example, and applies the example's comments and order.
- Bare keys without `=` are unset and receive the example value during synchronization.
- Review and edit the example to add or remove variables and update their comments or order. Do not add real credentials to it. Never manually copy values from a dotenv file into its example.
- The utility does not display values. Do not replace it with commands that print `.env` contents. If a local `.env` has no adjacent example yet, create its schema from a trusted source or ask the owner to supply it; do not inspect `.env` to reconstruct the schema.

## Utility behavior

- The utility accepts `.env`-prefixed names, including variants such as `.env.local`. It preserves quoted values and `#` characters inside values.
- It rejects unsupported syntax and duplicate keys before replacing the dotenv file. Writes use a temporary file and atomic replacement. New dotenv files are created with mode `0600`; existing file permissions are preserved.
- CLI output reports only the synchronized file path. Errors may report paths and line numbers but must not disclose dotenv contents.
