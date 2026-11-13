# Skill Authoring

Use this workflow when creating, revising, auditing, or installing personal agent skills.

## Required guidance

Before writing or revising a skill, read both complete skills below and apply them together:

- Canonical `$skill-creator`: package structure, resources, metadata, initialization, and validation.
- `$mattpocock-skills:writing-for-agents`: instruction hierarchy, context pointers, progressive disclosure, and pruning. Also read its `SKILL-MECHANICS.md` for skill invocation design.

The user's request controls the outcome. Neither skill expands authorization or the requested scope.

## Local workflow

1. Keep standalone sources at `skills/<skill-name>/` and T3 plugin sources at `t3-code-plugin/skills/<skill-name>/`. Resolve existing install links before editing a standalone skill.
2. For a new standalone installation, confirm the name is unused at both `~/.agents/skills/<skill-name>` and `~/.claude/skills/<skill-name>`. Link the agents path to the repository source and the Claude path to the agents link. Verify both resolve to the source. Change install links only when installation is in scope.
3. Keep planning and evaluation material outside the runtime skill unless an agent must load it while using the skill. Use `plans/` for active design work and `evaluations/` for external regression cases.
4. Run the canonical skill-creator `scripts/quick_validate.py` on each created or revised skill, plus the smallest relevant resource check. Plugin skills use the root `.claude-plugin/marketplace.json` catalog and the two manifests under `t3-code-plugin/`; install them through the plugin rather than adding per-skill links.

## T3 plugin tool-name check

Write concrete T3 tool references as standalone inline code, such as `t3_thread_read`. Keep action or parameter examples qualified, such as `action: "merge_back"`, so they are distinct from tool names. The check reads all plugin skill Markdown, including references, and checks those names against `Tool.make` definitions in the checkout's toolkit files and their directly imported tools.

From this repository, run:

```sh
python scripts/check-t3-tools.py /home/tnnrpolley21/Workspaces/Applications/t3code
```

Run it when validating the plugin and from the T3 fork's daily upstream sync after tool renames arrive. Wiring that external sync is separate from editing this repository.

Plugin caches, bundled `.system` skills, generated task artifacts, and copied install trees are not source locations.

## Review revisions

Compare every review-driven change with the original request and trigger cases. Remove review-created machinery when it no longer serves them; do not preserve rejected drafts as current guidance.
