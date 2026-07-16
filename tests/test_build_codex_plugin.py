from __future__ import annotations

import importlib.util
import json
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
