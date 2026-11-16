# Project instructions

## Environment files

- Never read, inspect, print, or put the contents of a real `.env` file into LLM context. This applies to all `.env` filename variants, including nested files. Do not run tools or commands that expose their values in output, logs, diffs, or generated context. File paths may be listed; values must not be displayed.
- Before creating, updating, synchronizing, or troubleshooting dotenv files, read and follow the [safe-dotenv instructions](skills/safe-dotenv/SKILL.md).

## Reusing instructions

If the instructions for a referenced skill or rule are already in context and unchanged, reuse them, even when another skill asks you to load them. Otherwise, load them using the agent's supported mechanism. Reload them after context loss or a change.
