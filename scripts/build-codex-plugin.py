#!/usr/bin/env python3
"""Build the promoted skill set as a native Codex plugin."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile


class BuildError(RuntimeError):
    """Raised when source skills cannot produce a valid plugin."""


@dataclass(frozen=True)
class SourceSkill:
    name: str
    source: Path


def load_source_manifest(repo_root: Path) -> dict[str, object]:
    path = repo_root.resolve() / ".claude-plugin" / "plugin.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise BuildError(f"unable to read {path}: {error}") from error
    if not isinstance(payload, dict):
        raise BuildError(f"{path}: manifest must be a JSON object")
    skills = payload.get("skills")
    if not isinstance(skills, list) or not skills:
        raise BuildError(f"{path}: skills must be a non-empty array")
    return payload


def select_skills(repo_root: Path, manifest: dict[str, object]) -> list[SourceSkill]:
    root = repo_root.resolve()
    raw_skills = manifest.get("skills")
    if not isinstance(raw_skills, list) or not raw_skills:
        raise BuildError("source manifest skills must be a non-empty array")

    selected: list[SourceSkill] = []
    names: set[str] = set()
    for raw_path in raw_skills:
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise BuildError("source manifest skill paths must be non-empty strings")
        source = (root / raw_path).resolve()
        if not source.is_relative_to(root):
            raise BuildError(f"skill source is outside repository: {raw_path}")
        if not source.is_dir():
            raise BuildError(f"skill source does not exist: {raw_path}")
        if not (source / "SKILL.md").is_file():
            raise BuildError(f"skill source is missing SKILL.md: {raw_path}")
        name = source.name
        if name in names:
            raise BuildError(f"duplicate skill name after flattening: {name}")
        names.add(name)
        selected.append(SourceSkill(name=name, source=source))
    return selected


def normalize_skill_markdown(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise BuildError("SKILL.md must start with YAML frontmatter")
    closing = next(
        (
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.rstrip("\r\n") == "---"
        ),
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


def _required(manifest: dict[str, object], field: str) -> object:
    value = manifest.get(field)
    if value in (None, "", [], {}):
        raise BuildError(f"source manifest field is required: {field}")
    return value


def _plugin_manifest(source: dict[str, object]) -> dict[str, object]:
    return {
        "name": _required(source, "name"),
        "version": _required(source, "version"),
        "description": _required(source, "description"),
        "author": _required(source, "author"),
        "homepage": _required(source, "homepage"),
        "repository": "https://github.com/tannerpolley/skills",
        "license": _required(source, "license"),
        "keywords": _required(source, "keywords"),
        "skills": "./skills/",
        "interface": {
            "displayName": "Matt Pocock Skills",
            "shortDescription": "Engineering workflows for real applications",
            "longDescription": (
                "Reusable workflows for planning, testing, debugging, reviewing, "
                "and maintaining applications."
            ),
            "developerName": "Matt Pocock",
            "category": "Developer Tools",
            "capabilities": ["Interactive", "Write"],
            "websiteURL": "https://www.aihero.dev",
            "defaultPrompt": ["Ask which engineering workflow fits this task."],
        },
    }


def _prepare_output(repo_root: Path, output_root: Path) -> None:
    root = repo_root.resolve()
    output = output_root.resolve()
    if output == root or root.is_relative_to(output):
        raise BuildError(f"refusing to replace repository or its parent: {output}")
    if output.is_relative_to(root) and not output.is_relative_to(root / "plugins"):
        raise BuildError(f"output inside repository must be under plugins: {output}")
    if output.exists():
        if not output.is_dir():
            raise BuildError(f"output path is not a directory: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)


def build_plugin(repo_root: Path, output_root: Path) -> int:
    root = repo_root.resolve()
    output = output_root.resolve()
    source_manifest = load_source_manifest(root)
    selected = select_skills(root, source_manifest)
    manifest = _plugin_manifest(source_manifest)
    normalized_markdown = {
        skill.name: normalize_skill_markdown(
            (skill.source / "SKILL.md").read_text(encoding="utf-8")
        )
        for skill in selected
    }
    _prepare_output(root, output)

    manifest_dir = output / ".codex-plugin"
    manifest_dir.mkdir()
    (manifest_dir / "plugin.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    skills_root = output / "skills"
    skills_root.mkdir()
    for skill in selected:
        destination = skills_root / skill.name
        shutil.copytree(skill.source, destination)
        skill_markdown = destination / "SKILL.md"
        skill_markdown.write_text(
            normalized_markdown[skill.name],
            encoding="utf-8",
        )

    sources = "\n".join(
        f"- `{skill.source.relative_to(root).as_posix()}`" for skill in selected
    )
    (output / "GENERATED.md").write_text(
        "# Generated Codex plugin\n\n"
        "Do not edit this directory by hand. Regenerate it with "
        "`python3 scripts/build-codex-plugin.py`.\n\n"
        "The source allowlist is `.claude-plugin/plugin.json`.\n\n"
        "## Included skills\n\n"
        f"{sources}\n",
        encoding="utf-8",
    )
    return len(selected)


def _file_digests(root: Path) -> dict[str, str]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def tree_diff(expected: Path, actual: Path) -> list[str]:
    expected_files = _file_digests(expected)
    actual_files = _file_digests(actual)
    differences: list[str] = []
    for path in sorted(expected_files.keys() - actual_files.keys()):
        differences.append(f"added: {path}")
    for path in sorted(expected_files.keys() & actual_files.keys()):
        if expected_files[path] != actual_files[path]:
            differences.append(f"changed: {path}")
    for path in sorted(actual_files.keys() - expected_files.keys()):
        differences.append(f"removed: {path}")
    return differences


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_root)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    output = args.output or repo_root / "plugins" / "mattpocock-skills"
    if not output.is_absolute():
        output = repo_root / output
    output = output.resolve()
    try:
        if args.check:
            with tempfile.TemporaryDirectory(prefix="mattpocock-codex-plugin-") as temp:
                expected = Path(temp) / "plugin"
                build_plugin(repo_root, expected)
                differences = tree_diff(expected, output)
            if differences:
                print("Generated Codex plugin is stale:")
                for difference in differences:
                    print(difference)
                return 1
            print(f"Generated Codex plugin is current: {output}")
            return 0

        count = build_plugin(repo_root, output)
        print(f"Generated {count} skills at {output}")
        return 0
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
