# Native Codex Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the repository's 22 promoted skills as one installable, generated, and drift-checked Codex plugin.

**Architecture:** A Python standard-library generator reads the existing Claude plugin allowlist, validates and flattens the selected skill directories, removes two Claude-only frontmatter fields from generated copies, and writes a Codex manifest. The repository commits the generated plugin tree and a root marketplace entry; unit tests, CI, Codex validators, and an isolated installation prove the artifact.

**Tech Stack:** Python 3 standard library, `unittest`, JSON, GitHub Actions, Codex CLI

## Global Constraints

- Keep `.claude-plugin/plugin.json` as the promoted-skill allowlist and metadata source.
- Include exactly the 22 promoted skills selected by that allowlist.
- Preserve the canonical bucketed directories under `skills/`.
- Remove only `disable-model-invocation` and `argument-hint` from generated `SKILL.md` frontmatter.
- Preserve each skill's scripts, references, assets, and `agents/openai.yaml`.
- Add no MCP server, connector, hook, upstream pull request, or public-directory submission.
- Use Python's standard library; add no runtime dependency.

---

### Task 1: Build and validate the generator core

**Files:**
- Create: `scripts/build-codex-plugin.py`
- Create: `tests/test_build_codex_plugin.py`

**Interfaces:**
- Consumes: `.claude-plugin/plugin.json` field `skills: list[str]`
- Produces: `SourceSkill(name: str, source: Path)`, `load_source_manifest(repo_root: Path) -> dict`, `select_skills(repo_root: Path, manifest: dict) -> list[SourceSkill]`, and `normalize_skill_markdown(text: str) -> str`

- [ ] **Step 1: Write failing unit tests for allowlist selection and frontmatter normalization**

Add tests that load the real manifest, assert 22 unique source skills, assert every source contains `SKILL.md`, and verify this transformation:

```python
source = """---
name: example
description: Example skill.
argument-hint: "[topic]"
disable-model-invocation: true
---

Instructions.
"""

expected = """---
name: example
description: Example skill.
---

Instructions.
"""

self.assertEqual(module.normalize_skill_markdown(source), expected)
```

Add temporary-repository tests that assert `select_skills` raises `BuildError` for a missing skill, a path outside the repository, a missing `SKILL.md`, and two selected directories with the same basename.

- [ ] **Step 2: Run the focused tests and confirm they fail**

Run: `python3 -m unittest -v tests.test_build_codex_plugin`

Expected: `ModuleNotFoundError` or missing-function failures for `build-codex-plugin.py`.

- [ ] **Step 3: Implement the validated source model and normalization**

Implement:

```python
@dataclass(frozen=True)
class SourceSkill:
    name: str
    source: Path


class BuildError(RuntimeError):
    pass


def load_source_manifest(repo_root: Path) -> dict[str, object]:
    path = repo_root / ".claude-plugin" / "plugin.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload.get("skills"), list) or not payload["skills"]:
        raise BuildError(f"{path}: skills must be a non-empty array")
    return payload


def normalize_skill_markdown(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise BuildError("SKILL.md must start with YAML frontmatter")
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.rstrip("\r\n") == "---"),
        None,
    )
    if closing is None:
        raise BuildError("SKILL.md frontmatter is not closed")
    blocked = ("disable-model-invocation:", "argument-hint:")
    return "".join(
        line
        for index, line in enumerate(lines)
        if not (index < closing and line.lstrip().startswith(blocked))
    )
```

Resolve every allowlist entry, require it to remain under `repo_root`, require `SKILL.md`, and reject duplicate basenames.

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `python3 -m unittest -v tests.test_build_codex_plugin`

Expected: all Task 1 tests pass.

- [ ] **Step 5: Commit the generator core**

```bash
git add scripts/build-codex-plugin.py tests/test_build_codex_plugin.py
git commit -m "feat: add Codex plugin generator core"
```

### Task 2: Generate a deterministic Codex plugin and detect drift

**Files:**
- Modify: `scripts/build-codex-plugin.py`
- Modify: `tests/test_build_codex_plugin.py`
- Create: `.agents/plugins/marketplace.json`
- Create: `plugins/mattpocock-skills/.codex-plugin/plugin.json`
- Create: `plugins/mattpocock-skills/GENERATED.md`
- Create: `plugins/mattpocock-skills/skills/*`

**Interfaces:**
- Consumes: Task 1 functions and the source manifest
- Produces: `build_plugin(repo_root: Path, output_root: Path) -> None`, `tree_diff(expected: Path, actual: Path) -> list[str]`, and CLI options `--repo-root`, `--output`, and `--check`

- [ ] **Step 1: Write failing generation and drift tests**

Add tests that build into `TemporaryDirectory`, then assert:

```python
self.assertEqual(len(list((output / "skills").iterdir())), 22)
self.assertEqual(
    json.loads((output / ".codex-plugin" / "plugin.json").read_text())["skills"],
    "./skills/",
)
self.assertFalse(any("disable-model-invocation:" in path.read_text() for path in output.glob("skills/*/SKILL.md")))
self.assertTrue((output / "skills" / "ask-matt" / "agents" / "openai.yaml").is_file())
```

Add a test that changes one generated file and asserts `tree_diff` reports it. Add a CLI test that expects `--check` to exit 1 for drift and 0 after regeneration.

- [ ] **Step 2: Run the focused tests and confirm they fail**

Run: `python3 -m unittest -v tests.test_build_codex_plugin`

Expected: missing `build_plugin` and `tree_diff` failures.

- [ ] **Step 3: Implement deterministic generation and check mode**

`build_plugin` must create a fresh output tree, copy each selected source with `shutil.copytree`, normalize only generated `SKILL.md`, and write sorted, indented JSON with a trailing newline.

Build the manifest from the source manifest:

```python
manifest = {
    "name": source["name"],
    "version": source["version"],
    "description": source["description"],
    "author": source["author"],
    "homepage": source["homepage"],
    "repository": "https://github.com/tannerpolley/skills",
    "license": source["license"],
    "keywords": source["keywords"],
    "skills": "./skills/",
    "interface": {
        "displayName": "Matt Pocock Skills",
        "shortDescription": "Engineering workflows for real applications",
        "longDescription": "Reusable workflows for planning, testing, debugging, reviewing, and maintaining applications.",
        "developerName": "Matt Pocock",
        "category": "Developer Tools",
        "capabilities": ["Interactive", "Write"],
        "websiteURL": "https://www.aihero.dev",
        "defaultPrompt": ["Ask which engineering workflow fits this task."],
    },
}
```

`tree_diff` must compare relative file inventories and SHA-256 digests, returning messages prefixed with `added:`, `removed:`, or `changed:`. Check mode builds in a temporary directory and prints every difference without touching the tracked output.

- [ ] **Step 4: Add the marketplace and generate the tracked artifact**

Create `.agents/plugins/marketplace.json`:

```json
{
  "name": "tannerpolley-skills",
  "interface": {
    "displayName": "Tanner Polley Skills"
  },
  "plugins": [
    {
      "name": "mattpocock-skills",
      "source": {
        "source": "local",
        "path": "./plugins/mattpocock-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Developer Tools"
    }
  ]
}
```

Run: `python3 scripts/build-codex-plugin.py`

Expected: the generator reports 22 skills written under `plugins/mattpocock-skills`.

- [ ] **Step 5: Run tests and drift validation**

Run:

```bash
python3 -m unittest -v tests.test_build_codex_plugin
python3 scripts/build-codex-plugin.py --check
```

Expected: all tests pass and check mode reports that generated output is current.

- [ ] **Step 6: Commit the generated distribution**

```bash
git add scripts/build-codex-plugin.py tests/test_build_codex_plugin.py .agents/plugins/marketplace.json plugins/mattpocock-skills
git commit -m "feat: generate native Codex plugin"
```

### Task 3: Document and continuously verify Codex installation

**Files:**
- Modify: `README.md`
- Create: `.github/workflows/codex-plugin.yml`

**Interfaces:**
- Consumes: `.agents/plugins/marketplace.json`, generated plugin tree, generator CLI
- Produces: user installation commands and CI proof of generation plus Codex namespace discovery

- [ ] **Step 1: Write the README installation and maintenance section**

Document:

```bash
codex plugin marketplace add tannerpolley/skills
codex plugin add mattpocock-skills@tannerpolley-skills
```

Explain that the plugin contains the promoted set, generated files must not be edited, `python3 scripts/build-codex-plugin.py` regenerates them, and `python3 scripts/build-codex-plugin.py --check` detects drift.

- [ ] **Step 2: Add CI for unit tests, drift, and isolated installation**

Create a workflow that runs on pushes and pull requests:

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
- uses: actions/setup-node@v4
  with:
    node-version: "22"
- run: python3 -m unittest -v tests.test_build_codex_plugin
- run: python3 scripts/build-codex-plugin.py --check
- run: npm install --global @openai/codex
- run: |
    export CODEX_HOME="$RUNNER_TEMP/codex-home"
    mkdir -p "$CODEX_HOME"
    codex plugin marketplace add "$GITHUB_WORKSPACE"
    codex plugin add mattpocock-skills@tannerpolley-skills
    codex debug prompt-input "test" | grep -q 'mattpocock-skills:code-review'
```

- [ ] **Step 3: Run local documentation and workflow checks**

Run:

```bash
python3 -m unittest -v tests.test_build_codex_plugin
python3 scripts/build-codex-plugin.py --check
python3 -c 'import yaml; yaml.safe_load(open(".github/workflows/codex-plugin.yml"))'
git diff --check
```

Expected: tests and drift check pass, workflow YAML parses, and Git reports no whitespace errors.

- [ ] **Step 4: Commit documentation and CI**

```bash
git add README.md .github/workflows/codex-plugin.yml
git commit -m "docs: add Codex plugin installation workflow"
```

### Task 4: Validate, publish, and close the governed outcome

**Files:**
- Modify only if verification finds a defect in the files above.

**Interfaces:**
- Consumes: complete branch and issue #1 acceptance criteria
- Produces: passing local evidence, pushed commits, a fork pull request, and verified issue closeout

- [ ] **Step 1: Run Codex validators**

Run:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/mattpocock-skills
for skill in plugins/mattpocock-skills/skills/*; do
  python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" "$skill"
done
```

Expected: the plugin and all 22 generated skills pass.

- [ ] **Step 2: Run an isolated marketplace installation**

Run with a temporary `CODEX_HOME`, then assert installed state and namespaced prompt discovery:

```bash
CODEX_HOME="$tmp/codex-home" codex plugin marketplace add "$PWD" --json
CODEX_HOME="$tmp/codex-home" codex plugin add mattpocock-skills@tannerpolley-skills --json
CODEX_HOME="$tmp/codex-home" codex plugin list --json
CODEX_HOME="$tmp/codex-home" codex debug prompt-input "test"
```

Expected: installation reports version `1.2.0`, plugin state is enabled, and prompt input contains names beginning with `mattpocock-skills:`.

- [ ] **Step 3: Run full repository verification and cleanup**

Run:

```bash
python3 -m unittest -v tests.test_build_codex_plugin
python3 scripts/build-codex-plugin.py --check
git diff --check
bash "$HOME/.codex/hooks/codex-cleanup.sh" --repo-root .
git status --short --branch
```

Expected: all checks pass and the worktree contains only intentional committed changes.

- [ ] **Step 4: Push and open the fork pull request**

Push the implementation branch to `origin`, open a pull request against `tannerpolley/skills:main` with `Closes #1`, and re-read PR checks.

- [ ] **Step 5: Merge after checks pass and verify closeout**

Merge the fork pull request, verify `main` contains the merge commit, verify issue #1 closed through the PR, and run the Project Truss closeout audit from fresh GitHub and Git evidence.
