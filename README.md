# Personal agent skills

Canonical workspace for personal skills used by Codex and Claude. Standalone sources live in `skills/`; Codex discovers them through `~/.agents/skills/<name>` links to this repository, and Claude through `~/.claude/skills/<name>` links to the agents links.

The `t3-code` plugin lives in `t3-code-plugin/`, with five skills: threads, issues, handoff, artifacts and notebooks. Both agents use the root `.claude-plugin/marketplace.json` catalog (`tannerpolley-skills`). Plugin skills are installed through that catalog rather than individual skill links.

See [skill authoring](docs/skill-authoring.md) for the required guidance and tool-name check. Regression cases outside runtime skills live in `evaluations/`.
