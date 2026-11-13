# Personal skill workspace

This repository is the source of truth for personal agent skills created or revised on this machine.

## Layout

- Keep standalone skills in `skills/<skill-name>/` and T3 plugin skills in `t3-code-plugin/skills/<skill-name>/`.
- Keep task-specific design notes in `plans/` only when a plan is requested or needed.
- Expose standalone skills through `~/.agents/skills/<skill-name>` → repository source and `~/.claude/skills/<skill-name>` → the agents link. Install plugin skills through the plugin catalog.

## Skill work

For every skill creation or revision, first read both the complete canonical `$skill-creator` skill and the complete `$mattpocock-skills:writing-for-agents` skill, including `SKILL-MECHANICS.md`. Apply them together: skill-creator owns package structure and validation; writing-for-agents owns agent-facing instruction and pointer design. Then follow [the local authoring workflow](docs/skill-authoring.md).

1. Read the complete existing skill and every directly linked instruction before editing it.
2. Make the smallest change that satisfies the request; add scripts, references, assets, or metadata only when they have a concrete use.
3. Keep one authoritative copy in the appropriate repository skill folder. Installed links and plugin caches are not editable sources.
4. For a new standalone skill, confirm the destination name is unused in both link locations before creating links.
5. Run the skill-creator validator. For standalone installation work, verify both links resolve to the repository copy; for plugin work, follow the checks in the local authoring workflow, and after merging to `main` run `scripts/refresh-t3-plugin.sh` from the main checkout so both agents load the change.

Do not modify a harness's managed `.system` skills or plugin cache as part of ordinary local skill work.
