---
name: git-commit-hygiene
description: Prepare atomic Git commits, write commit messages, and keep unpublished history focused. Use when creating or splitting commits, writing commit messages, or cleaning up local history.
---

# Git commit hygiene

- Make each commit atomic and focused on one change. Keep its code, tests, and documentation together. Split unrelated changes into separate commits.
- Do not use Conventional Commit prefixes such as `feat:` or `fix:`.
- Write a capitalized, imperative subject that concisely describes the change, aiming for 50 characters or fewer.
- When explanation is needed, separate the body from the subject with a blank line, wrap it at about 72 characters, and explain the motivation and how behavior differs from before.
- Check the changes being committed for whitespace errors.

## Unpublished history

- Keep unpublished history focused before publishing or when preparing further commits.
- Drop changes and reversals that cancel out, or absorb the reversal into the original change when appropriate.
- Fold related small adjustments into the commit they improve, even when unrelated commits occur between them. Preserve dependencies, the intended final tree, and coherent commit boundaries.
- Rewrite history only when the affected commits are known to be unpublished and unshared. Ask before rewriting someone else's commits or when their publication status is uncertain.

Based on Pro Git's commit guidelines.
