# Native Codex Plugin Design

Issue: [#1](https://github.com/tannerpolley/skills/issues/1)

## Goal

Ship the repository's 22 promoted skills as one native Codex plugin without changing the bucketed source layout used for authoring and Claude Code distribution.

## Selected approach

Commit a generated plugin under `plugins/mattpocock-skills/`. A Python generator reads the existing skill allowlist from `.claude-plugin/plugin.json`, copies each selected skill into a flat `skills/<name>/` directory, and writes the Codex manifest. The generated tree remains reviewable in Git and installable from a Git marketplace snapshot.

The generator treats the bucketed directories as the source of truth. It removes the Claude-only `disable-model-invocation` and `argument-hint` frontmatter fields from generated `SKILL.md` files. It preserves `agents/openai.yaml`, including `policy.allow_implicit_invocation`, so user-invoked skills keep the intended Codex behavior.

## Alternatives considered

### Point Codex at the repository's `skills/` directory

This requires little code, but it publishes all 41 skills. Users would receive deprecated, personal, miscellaneous, and unfinished workflows. The strict plugin validator also expects each immediate child of the plugin's `skills/` directory to contain `SKILL.md`, while the repository uses bucket directories.

### Move non-promoted skills outside `skills/`

This would let Codex scan the remaining tree, but it would disrupt authoring paths, documentation links, helper scripts, and upstream synchronization.

### Generate the promoted plugin tree

This keeps upstream paths intact and produces a validator-friendly artifact. A check mode and CI prevent generated copies from drifting. This approach adds generated files, but the repository never edits them by hand.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/mattpocock-skills/
├── .codex-plugin/plugin.json
└── skills/
    ├── ask-matt/
    ├── code-review/
    └── ...
scripts/build-codex-plugin.py
tests/test_build_codex_plugin.py
```

The marketplace contains one local entry whose source path is `./plugins/mattpocock-skills`. Codex resolves that path from the marketplace repository root.

## Generator contract

The generator will:

1. Read `.claude-plugin/plugin.json` and require a non-empty array of skill directories.
2. Reject missing source skills, duplicate skill names, paths outside the repository, and missing `SKILL.md` files.
3. Copy every selected skill directory, including scripts, references, assets, and `agents/openai.yaml`.
4. Remove only `disable-model-invocation` and `argument-hint` from the YAML frontmatter of generated `SKILL.md` files.
5. Write `.codex-plugin/plugin.json` with `skills` set to `./skills/` and metadata derived from the Claude manifest.
6. Support `--check`, which builds into a temporary directory and reports drift without changing tracked files.

Generated output will include a marker file that identifies the generator and source allowlist. Contributors regenerate the plugin after changing a promoted skill or the Claude manifest.

## Error handling

The generator exits nonzero with a specific path or field when source data is invalid. Check mode lists added, removed, and changed paths. It does not repair output unless run without `--check`.

The CI workflow fails on source/output drift, unit-test failures, invalid skill frontmatter, a failed isolated plugin install, or missing namespaced skill discovery.

## Testing

Unit tests will cover:

- the promoted skill count and names;
- flattening and resource copying;
- removal of Claude-only frontmatter;
- preservation of Codex invocation metadata;
- duplicate-name and missing-source failures;
- check-mode drift detection.

Repository validation will run the generator in check mode, the Codex plugin validator when available, the Codex skill validator for every generated skill when available, and an isolated `CODEX_HOME` marketplace install. The isolated test will inspect `codex debug prompt-input` for the `mattpocock-skills:` namespace.

## Documentation and release behavior

The README will explain installation from `tannerpolley/skills`, regeneration, and validation. The Codex manifest version follows `.claude-plugin/plugin.json`; this work does not repair the existing version mismatch between that file and `package.json` because the mismatch predates the fork change and does not affect the Codex artifact.

No upstream pull request, public directory submission, connector, MCP server, or hook is part of this change.
