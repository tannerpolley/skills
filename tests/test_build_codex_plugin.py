from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build-codex-plugin.py"


def load_module():
    if not MODULE_PATH.is_file():
        raise AssertionError(f"missing generator: {MODULE_PATH}")
    spec = importlib.util.spec_from_file_location("build_codex_plugin", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load generator: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_manifest(root: Path, skills: list[str]) -> None:
    manifest_dir = root / ".claude-plugin"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps({"skills": skills}),
        encoding="utf-8",
    )


def write_skill(root: Path, relative: str, name: str = "example") -> Path:
    skill = root / relative
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Example skill.\n---\n\nInstructions.\n",
        encoding="utf-8",
    )
    return skill


class SourceSelectionTests(unittest.TestCase):
    def test_real_manifest_selects_22_unique_skills(self) -> None:
        module = load_module()

        manifest = module.load_source_manifest(REPO_ROOT)
        selected = module.select_skills(REPO_ROOT, manifest)

        self.assertEqual(len(selected), 22)
        self.assertEqual(len({skill.name for skill in selected}), 22)
        self.assertTrue(all((skill.source / "SKILL.md").is_file() for skill in selected))

    def test_missing_source_is_rejected(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_manifest(root, ["./skills/engineering/missing"])

            with self.assertRaisesRegex(module.BuildError, "does not exist"):
                module.select_skills(root, module.load_source_manifest(root))

    def test_source_outside_repository_is_rejected(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent / "repo"
            root.mkdir()
            outside = write_skill(parent, "outside")
            write_manifest(root, [str(outside)])

            with self.assertRaisesRegex(module.BuildError, "outside repository"):
                module.select_skills(root, module.load_source_manifest(root))

    def test_source_without_skill_markdown_is_rejected(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "skills" / "engineering" / "empty").mkdir(parents=True)
            write_manifest(root, ["./skills/engineering/empty"])

            with self.assertRaisesRegex(module.BuildError, "missing SKILL.md"):
                module.select_skills(root, module.load_source_manifest(root))

    def test_duplicate_flattened_names_are_rejected(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill(root, "skills/engineering/example")
            write_skill(root, "skills/productivity/example")
            write_manifest(
                root,
                ["./skills/engineering/example", "./skills/productivity/example"],
            )

            with self.assertRaisesRegex(module.BuildError, "duplicate skill name"):
                module.select_skills(root, module.load_source_manifest(root))


class FrontmatterNormalizationTests(unittest.TestCase):
    def test_claude_only_fields_are_removed_from_frontmatter(self) -> None:
        module = load_module()
        source = """---
name: example
description: Example skill.
argument-hint: "[topic]"
disable-model-invocation: true
---

Instructions mention disable-model-invocation: true.
"""
        expected = """---
name: example
description: Example skill.
---

Instructions mention disable-model-invocation: true.
"""

        self.assertEqual(module.normalize_skill_markdown(source), expected)

    def test_missing_frontmatter_is_rejected(self) -> None:
        module = load_module()

        with self.assertRaisesRegex(module.BuildError, "start with YAML frontmatter"):
            module.normalize_skill_markdown("Instructions only.\n")

    def test_unclosed_frontmatter_is_rejected(self) -> None:
        module = load_module()

        with self.assertRaisesRegex(module.BuildError, "frontmatter is not closed"):
            module.normalize_skill_markdown("---\nname: example\n")


class PluginGenerationTests(unittest.TestCase):
    def test_build_plugin_generates_flat_promoted_bundle(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "plugin"

            module.build_plugin(REPO_ROOT, output)

            skill_roots = sorted(path for path in (output / "skills").iterdir() if path.is_dir())
            self.assertEqual(len(skill_roots), 22)
            self.assertTrue((output / "skills" / "ask-matt" / "agents" / "openai.yaml").is_file())
            self.assertTrue(
                (
                    output
                    / "skills"
                    / "diagnosing-bugs"
                    / "scripts"
                    / "hitl-loop.template.sh"
                ).is_file()
            )
            manifest = json.loads(
                (output / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["name"], "mattpocock-skills")
            self.assertEqual(manifest["version"], "1.2.0")
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["repository"], "https://github.com/tannerpolley/skills")
            self.assertTrue((output / "GENERATED.md").is_file())

    def test_generated_frontmatter_is_codex_specific(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "plugin"

            module.build_plugin(REPO_ROOT, output)

            generated = list(output.glob("skills/*/SKILL.md"))
            self.assertEqual(len(generated), 22)
            for path in generated:
                text = path.read_text(encoding="utf-8")
                frontmatter = text.split("---", 2)[1]
                self.assertNotIn("disable-model-invocation:", frontmatter, path)
                self.assertNotIn("argument-hint:", frontmatter, path)

    def test_tree_diff_reports_added_removed_and_changed_files(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected = root / "expected"
            actual = root / "actual"
            expected.mkdir()
            actual.mkdir()
            (expected / "added.txt").write_text("new\n", encoding="utf-8")
            (expected / "changed.txt").write_text("expected\n", encoding="utf-8")
            (actual / "changed.txt").write_text("actual\n", encoding="utf-8")
            (actual / "removed.txt").write_text("old\n", encoding="utf-8")

            differences = module.tree_diff(expected, actual)

            self.assertEqual(
                differences,
                [
                    "added: added.txt",
                    "changed: changed.txt",
                    "removed: removed.txt",
                ],
            )

    def test_cli_check_mode_detects_and_repairs_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "plugin"
            command = [
                sys.executable,
                str(MODULE_PATH),
                "--repo-root",
                str(REPO_ROOT),
                "--output",
                str(output),
            ]

            generated = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertIn("Generated 22 skills", generated.stdout)

            (output / "GENERATED.md").write_text("stale\n", encoding="utf-8")
            stale = subprocess.run(
                [*command, "--check"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(stale.returncode, 1)
            self.assertIn("changed: GENERATED.md", stale.stdout)

            regenerated = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(regenerated.returncode, 0, regenerated.stderr)
            current = subprocess.run(
                [*command, "--check"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(current.returncode, 0, current.stderr)
            self.assertIn("current", current.stdout)


class WorkflowTests(unittest.TestCase):
    def test_namespace_check_does_not_pipe_prompt_into_grep_q(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "codex-plugin.yml").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("| grep -q", workflow)
        self.assertIn(
            'codex debug prompt-input "test" > "$RUNNER_TEMP/codex-prompt.json"',
            workflow,
        )
        self.assertIn(
            "grep -q 'mattpocock-skills:code-review' \"$RUNNER_TEMP/codex-prompt.json\"",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
