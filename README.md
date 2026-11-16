# my-skills

Opinionated agent workflows to understand and adapt to your project.

## Philosophy

- These skills describe my workflows. They won't fit every project, so don't apply them blindly.
- Read each skill you intend to use, including its supporting files, and understand what it does.
- Adapt skills to your project's conventions and constraints. Keep the adopted copies editable instead of treating them as immutable packages. [adopt-skill](skills/adopt-skill/SKILL.md) helps with this.

## Skills

Repository license: [MIT](LICENSE).

| Skill | Purpose | Notes | License and credit |
| --- | --- | --- | --- |
| [adopt-skill](skills/adopt-skill/SKILL.md) | Adapt skills to a project. | Checks for conflicts before adoption. | [MIT](skills/adopt-skill/LICENSE) |
| [diataxis-documentation](skills/diataxis-documentation/SKILL.md) | Maintain Diátaxis documentation. | Can use artifacts from Matt Pocock's [domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling) and [grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs). The latter uses domain-modeling and [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling). None is required or included. | [MIT](skills/diataxis-documentation/LICENSE); adapted from [GitHub's documentation-writer](https://github.com/github/awesome-copilot/tree/main/skills/documentation-writer) ([MIT](skills/diataxis-documentation/references/AWESOME-COPILOT-LICENSE)); includes [Unslop](https://github.com/poteto/noodle) ([MIT](skills/diataxis-documentation/references/UNSLOP-LICENSE)). |
| [safe-dotenv](skills/safe-dotenv/SKILL.md) | Reduce the risk of exposing dotenv contents. | Synchronizes adjacent examples and adds an always-on safeguard when adopted. Protection is best effort, not guaranteed. | [MIT](skills/safe-dotenv/LICENSE) |
| [git-commit-hygiene](skills/git-commit-hygiene/SKILL.md) | Create focused commits and keep unpublished history clean. | No Conventional Commit prefixes. | [MIT](skills/git-commit-hygiene/LICENSE) |
| [justfile-conventions](skills/justfile-conventions/SKILL.md) | Write consistent justfiles. | Uses lowercase `justfile` and supports native dotenv loading. | [MIT](skills/justfile-conventions/LICENSE) |

## Adopt skills

Install the adoption skill in the target project. If a skill named `adopt-skill` already exists there, resolve the name collision before running this command.

```sh
npx --yes skills add https://github.com/fardjad/my-skills --skill adopt-skill --agent universal -y
```

Read `adopt-skill`, then ask your agent to adopt the skills you want:

```text
Use adopt-skill to adopt safe-dotenv and git-commit-hygiene from https://github.com/fardjad/my-skills into this project.
```

Review the proposed changes and the resulting skills before using them.

