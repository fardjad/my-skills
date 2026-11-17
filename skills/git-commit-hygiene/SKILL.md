---
name: git-commit-hygiene
description: Prepare atomic Git commits, write commit messages, keep unpublished history focused, and integrate changes with linear history. Use when creating or splitting commits, writing commit messages, cleaning up local history, or integrating changes into a target branch.
---

# Git commit hygiene

- Make each commit atomic and focused on one change. Keep its code, tests, and documentation together. Split unrelated changes into separate commits.
- Do not use Conventional Commit prefixes such as `feat:` or `fix:`.
- Write a capitalized, imperative subject that concisely describes the change, aiming for 50 characters or fewer.
- When explanation is needed, separate the body from the subject with a blank line, wrap it at about 72 characters, and explain the motivation and how behavior differs from before.
- When project policy or a request requires issue references, put them in a separate commit footer, not in the subject or body. Separate the footer with a blank line, for example `Jira-ref: XYZ-123`.
- Check the changes being committed for whitespace errors.

## Unpublished history

- Keep unpublished history focused before publishing or when preparing further commits.
- Drop changes and reversals that cancel out, or absorb the reversal into the original change when appropriate.
- Fold related small adjustments into the commit they improve, even when unrelated commits occur between them. Preserve dependencies, the intended final tree, and coherent commit boundaries.
- Rewrite history only when the affected commits are known to be unpublished and unshared. Ask before rewriting someone else's commits or when their publication status is uncertain.

## Integrating changes

- Prefer linear history: integrate changes using rebase, cherry-pick, or squash rather than merge commits. Update the target branch by fast-forwarding it.
- Validate the changes against the current target branch tip. If the tip advances before the target branch is updated, incorporate the new tip into the changes and revalidate before updating the target branch. Do not force-update the target branch unless the user explicitly requests or confirms it.

Based on Pro Git's commit guidelines.
