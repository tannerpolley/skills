#!/usr/bin/env python3
"""Build the promoted skill set as a native Codex plugin."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


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
