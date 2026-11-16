---
name: diataxis-documentation
description: Write and maintain accurate Diátaxis documentation for users and maintainers. Use for documentation changes or changes that affect documented behavior.
---

# Diátaxis documentation

When a change affects documented behavior, update the relevant existing documentation in the same change. Write clearly and accurately for the reader's goal, using consistent terminology and style. Verify technical details and examples.

## Diátaxis

Choose the document type for the reader's goal:

- Tutorials teach through practical steps.
- How-to guides give steps for a specific problem.
- Reference describes the machinery.
- Explanation clarifies a topic.

## Locations

Keep separate audience trees: `docs/maintainers/` for project and repository maintainers, and `docs/user/` for users. Within each, place content under `tutorials/`, `how-to/`, `reference/`, or `explanation/`. Create directories when they have content.

## Workflow

Apply the bundled [Unslop guidance](references/unslop.md) when writing or editing prose. Reuse it if it is already in the current context and unchanged; otherwise load it.

For routine updates to existing documentation and small inline changes, write directly without a new outline or approval.

For new standalone documentation:

1. Determine the document type, target audience, reader's goal, and scope, including exclusions. Ask about any gaps.
2. Propose an outline and wait for approval before writing the full document.
3. Write the approved documentation in Markdown using the principles above.

## Context and sources

Use relevant local files as sources and supplied Markdown for tone, style, and terminology. Don't copy prose from supplied Markdown unless explicitly asked. Consult external sources only when the user provides a link and asks you to use it.

Use these domain documents when they exist:

- If `GLOSSARY-MAP.md` exists, follow it to the relevant context glossaries; otherwise, use the root `GLOSSARY.md` if present. Use the preferred terms and respect context-specific meanings.
- Consult relevant system-wide and context-specific ADRs, including those under `docs/adr/`. Account for a decision's status when provided, and use its rationale when explaining the design.
- Cross-check these artifacts against current behavior and flag contradictions or potentially stale decisions rather than presenting them as fact.

These artifacts are optional. Do not create or relocate them solely to write documentation, and do not require another skill to use them.
