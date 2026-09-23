#!/usr/bin/env python3
"""Report and clear disk space held by local coding-agent homes.

The default report writes nothing. --apply rebuildable deletes rebuildable
candidates; --apply all also deletes history candidates. A candidate must match
a rule below, be older than a day and its retention, resolve inside its agent
home, not be a symlink or a live database, and hold no file, working directory,
or executable in use by any process.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path

DAY = 86400
MIN_AGE_DAYS = 1  # a run may still be reading anything newer
LIVE_DB = re.compile(r"\.(sqlite|sqlite3|db)(-wal|-shm|-journal)?$")
REBUILDABLE, HISTORY = "rebuildable", "history"


@dataclass
class Rule:
    agent: str
    root: Path
    pattern: str  # glob relative to root; each match is one candidate
    kind: str
    days: int
    note: str
    keep: int = 0  # version folders: keep the newest `keep` plus the active one
    active: str | None = None  # name of the active version, if known


def link_name(path: Path) -> str | None:
    return path.resolve().name if path.is_symlink() else None


def t3_active(home: Path) -> str | None:
    try:
        state = json.loads((home / ".t3/runtime/service-state.json").read_text())
        return state.get("activeVersion")
    except (OSError, ValueError):
        return None


def rules(home: Path) -> list[Rule]:
    codex, claude, t3 = home / ".codex", home / ".claude", home / ".t3"
    return [
        Rule("codex", codex, "packages/standalone/releases/*", REBUILDABLE, MIN_AGE_DAYS,
             "old Codex version", keep=2, active=link_name(codex / "packages/standalone/current")),
        Rule("codex", codex, "archived_logs/*", REBUILDABLE, 14, "rotated log"),
        Rule("codex", codex, "archived_sessions/*", HISTORY, 30, "archived chat"),
        Rule("codex", codex, "archived_worktrees/*", HISTORY, 30,
             "moved-aside worktrees; may hold uncommitted work"),
        Rule("codex", codex, "backups/*", HISTORY, 30, "maintenance backup"),
        Rule("codex", codex, "visualizations/*", HISTORY, 30, "generated visualization"),
        Rule("codex", codex, "generated_images/*", HISTORY, 30, "generated image"),
        Rule("claude", home / ".local/share/claude", "versions/*", REBUILDABLE, MIN_AGE_DAYS,
             "old Claude Code version", keep=2, active=link_name(home / ".local/bin/claude")),
        Rule("claude", home / ".config/Claude", "claude-code/*", REBUILDABLE, MIN_AGE_DAYS,
             "old desktop-app Claude Code", keep=2),
        Rule("claude", claude, "debug/*", REBUILDABLE, 14, "debug log"),
        Rule("t3", t3, "runtime/versions/*", REBUILDABLE, MIN_AGE_DAYS,
             "old T3 runtime", keep=2, active=t3_active(home)),
        Rule("t3", t3, "userdata/logs/*.ndjson.*", REBUILDABLE, 14, "rotated trace log"),
        Rule("t3", t3, "userdata/logs/provider/*", REBUILDABLE, 14, "provider log"),
        Rule("t3", t3, "userdata/*.pre-*", HISTORY, 30, "database backup from a T3 upgrade"),
    ]


HOMES = {"codex": ".codex", "claude": ".claude", "t3": ".t3", "pi": ".pi"}


@dataclass
class Candidate:
    rule: Rule
    path: Path
    size: int
    age_days: float
    blocked: str = ""


def scan(path: Path) -> tuple[int, float]:
    """Disk usage in bytes and newest mtime, without following symlinks."""
    st = path.lstat()
    size, newest = st.st_blocks * 512, st.st_mtime
    if path.is_dir() and not path.is_symlink():
        for dirpath, dirs, files in os.walk(path):
            for name in dirs + files:
                try:
                    st = os.lstat(os.path.join(dirpath, name))
                except OSError:
                    continue
                size += st.st_blocks * 512
                newest = max(newest, st.st_mtime)
    return size, newest


def paths_in_use() -> set[str]:
    """Files, working directories, and executables held by any process."""
    used = set()
    for proc in Path("/proc").glob("[0-9]*"):
        for link in [proc / "cwd", proc / "exe", *_fds(proc)]:
            try:
                used.add(os.readlink(link))
            except OSError:
                pass
    return used


def _fds(proc: Path) -> list[Path]:
    try:
        return list((proc / "fd").iterdir())
    except OSError:
        return []


def version_key(name: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", name)]


def candidates(home: Path, now: float, in_use: set[str]) -> list[Candidate]:
    found = []
    for rule in rules(home):
        root = rule.root.resolve()
        matches = sorted((p for p in rule.root.glob(rule.pattern) if not p.is_symlink()),
                         key=lambda p: version_key(p.name))
        if rule.keep:
            kept = {p.name for p in matches[-rule.keep:]} | {rule.active}
            matches = [p for p in matches if p.name not in kept]
        for path in matches:
            if LIVE_DB.search(path.name) or not path.resolve().is_relative_to(root):
                continue
            size, newest = scan(path)
            age = (now - newest) / DAY
            if age < max(rule.days, MIN_AGE_DAYS):
                continue
            prefix = str(path) + os.sep
            busy = any(u == str(path) or u.startswith(prefix) for u in in_use)
            found.append(Candidate(rule, path, size, age, "in use by a running process" if busy else ""))
    return found


def missing_config_paths(home: Path) -> list[tuple[str, str]]:
    """(agent, description) for config entries that point at missing paths."""
    issues = []

    def walk(agent: str, value, where: str):
        if isinstance(value, dict):
            for key, item in value.items():
                walk(agent, item, f"{where}.{key}")
        elif isinstance(value, list):
            for item in value:
                walk(agent, item, where)
        elif isinstance(value, str):
            for token in re.split(r"[\s:]+", value):
                token = os.path.expanduser(token.strip("'\"{}[],"))
                if token.startswith(str(home)) and not Path(token).exists():
                    issues.append((agent, f"{where}: {token}"))

    codex_config = home / ".codex/config.toml"
    if codex_config.exists():
        config = tomllib.loads(codex_config.read_text())
        for project in stale_trusted_projects(config):
            issues.append(("codex", f"trusted project missing or temporary: {project}"))
        walk("codex", {k: v for k, v in config.items() if k != "projects"}, "config.toml")
    for agent, rel in [("claude", ".claude/settings.json"), ("pi", ".pi/agent/settings.json")]:
        try:
            walk(agent, json.loads((home / rel).read_text()), rel)
        except (OSError, ValueError):
            pass
    return issues


def stale_trusted_projects(config: dict) -> list[str]:
    return [p for p in config.get("projects", {})
            if not Path(p).exists() or p == "/tmp" or p.startswith("/tmp/")]


def fix_codex_trust(home: Path) -> list[str]:
    """Remove trusted-project blocks whose folder is missing or under /tmp."""
    path = home / ".codex/config.toml"
    text = path.read_text()
    stale = stale_trusted_projects(tomllib.loads(text))
    for project in stale:
        header = re.escape(f'[projects.{json.dumps(project)}]')
        text = re.sub(rf"^{header}\n(?:(?!\[).*\n)*", "", text, flags=re.M)
    tomllib.loads(text)  # refuse to write a config Codex could not parse
    tmp = path.with_name(path.name + ".agent-home-cleanup")
    tmp.write_text(text)
    os.chmod(tmp, path.stat().st_mode)
    os.replace(tmp, path)
    return stale


def home_sizes(home: Path) -> dict[str, int]:
    sizes = {}
    for agent, rel in HOMES.items():
        if (home / rel).exists():
            out = subprocess.run(["du", "-sb", str(home / rel)], capture_output=True, text=True).stdout
            sizes[agent] = int(out.split()[0]) if out else 0
    return sizes


def gb(n: int) -> str:
    return f"{n / 1e9:6.2f} GB"


def short(home: Path, path: Path) -> str:
    return "~/" + str(path.relative_to(home)) if path.is_relative_to(home) else str(path)


def report(home: Path, found: list[Candidate], issues: list[tuple[str, str]], list_all: bool) -> None:
    print("Agent homes")
    for agent, size in home_sizes(home).items():
        print(f"  {agent:7}{gb(size)}  ~/{HOMES[agent]}")
    for kind, heading in [(REBUILDABLE, "Rebuildable: cleared by --apply rebuildable and the weekly timer"),
                          (HISTORY, "History: cleared only by --apply all, after the user approves")]:
        rows = [c for c in found if c.rule.kind == kind and not c.blocked]
        print(f"\n{heading}  (total {gb(sum(c.size for c in rows)).strip()})")
        for rule in dict.fromkeys(c.rule.pattern for c in rows):
            group = sorted((c for c in rows if c.rule.pattern == rule), key=lambda c: -c.size)
            first = group[0]
            if len(group) > 8 and not list_all:
                ages = [c.age_days for c in group]
                print(f"  {first.rule.agent:7}{gb(sum(c.size for c in group))}  {len(group)} × {first.rule.note} "
                      f"({min(ages):.0f}–{max(ages):.0f} days): {short(home, first.rule.root / rule)}  (--list shows each)")
                continue
            for c in group:
                print(f"  {c.rule.agent:7}{gb(c.size)}  {c.age_days:4.0f} days  {c.rule.note}: {short(home, c.path)}")
                print(f"           rm -rf -- '{c.path}'")
    blocked = [c for c in found if c.blocked]
    if blocked:
        print("\nSkipped")
        for c in blocked:
            print(f"  {short(home, c.path)}: {c.blocked}")
    if issues:
        print("\nConfig entries pointing at missing paths (--fix-config removes the Codex trust entries)")
        for agent, issue in issues:
            print(f"  {agent:7}{issue}")


def apply(home: Path, found: list[Candidate], kinds: set[str]) -> int:
    in_use, freed = paths_in_use(), 0
    for c in found:
        if c.rule.kind not in kinds or c.blocked:
            continue
        prefix = str(c.path) + os.sep
        if any(u == str(c.path) or u.startswith(prefix) for u in in_use):
            print(f"skipped, now in use: {short(home, c.path)}")
            continue
        if c.path.is_dir():
            shutil.rmtree(c.path)
        else:
            c.path.unlink()
        freed += c.size
        print(f"deleted {gb(c.size).strip()}: {short(home, c.path)}")
    return freed


def notify(message: str) -> None:
    if shutil.which("notify-send"):
        subprocess.run(["notify-send", "Agent home cleanup", message], check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply", choices=[REBUILDABLE, "all"], help="delete candidates of this kind")
    parser.add_argument("--fix-config", action="store_true", help="remove missing or /tmp Codex trust entries")
    parser.add_argument("--notify", action="store_true", help="send a desktop notification summary")
    parser.add_argument("--list", action="store_true", help="list every candidate instead of grouping")
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    args = parser.parse_args()
    home = args.home

    found = candidates(home, time.time(), paths_in_use())
    if args.fix_config:
        for project in fix_codex_trust(home):
            print(f"removed Codex trust entry: {project}")
    if not args.apply:
        report(home, found, missing_config_paths(home), args.list)
        return 0

    before = sum(home_sizes(home).values())
    kinds = {REBUILDABLE} if args.apply == REBUILDABLE else {REBUILDABLE, HISTORY}
    freed = apply(home, found, kinds)
    after = sum(home_sizes(home).values())
    print(f"\nAgent homes: {gb(before).strip()} before, {gb(after).strip()} after; freed {gb(freed).strip()}")
    waiting = sum(c.size for c in found if c.rule.kind == HISTORY and HISTORY not in kinds and not c.blocked)
    if args.notify:
        notify(f"Freed {gb(freed).strip()} of rebuildable files."
               + (f" {gb(waiting).strip()} of old history awaits your approval: ask an agent to run agent-home-cleanup."
                  if waiting else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
