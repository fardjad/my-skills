---
name: adopt-skill
description: Adopt a skill into a project and check it against existing skills and instructions.
---

# Adopt a skill

If adopting multiple skills, follow these steps for each.

## Check

Read the requested skill and the files and scripts it uses. Identify dependencies on other skills and check applicable licenses.

Compare it with skills installed in the project and applicable rules and instructions, including `AGENTS.md`. Look for name collisions, conflicting instructions, overlapping triggers or workflows, and side effects that could interfere with each other.

## Resolve conflicts

When you find a conflict, show the relevant paths and ask the user how to resolve it:

1. Change the incoming skill.
2. Change the existing skills or rules.
3. Apply another solution the user chooses.

Wait for the user's decision before importing the affected skill or changing conflicting files.

## Adopt

Create an editable project-local copy with its required files, scripts, and applicable copyright and license notices. Preserve relative paths and executable permissions. If a required skill dependency is missing, tell the user and agree on how to handle it.

If a license is incompatible or permission is unclear, warn the user and ask how to proceed before copying the affected material.

Apply non-conflicting setup instructions and changes agreed with the user. Update references and run focused checks for changed scripts or behavior. Change existing skills or rules only when required for non-conflicting setup or approved by the user.
