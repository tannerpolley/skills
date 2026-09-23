"""Safety checks for agent_home_cleanup.py against a fake home. Run: python3 test_agent_home_cleanup.py"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "skills/agent-home-cleanup/scripts/agent_home_cleanup.py"
sys.path.insert(0, str(SCRIPT.parent))
import agent_home_cleanup as cleanup  # noqa: E402

DAY = 86400


def make(path: Path, age_days: float, folder: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not folder:
        path.write_text("x" * 4096)
    else:
        path.mkdir(exist_ok=True)
        (path / "payload").write_text("x" * 4096)
        os.utime(path / "payload", (time.time() - age_days * DAY,) * 2)
    os.utime(path, (time.time() - age_days * DAY,) * 2)
    return path


def main() -> None:
    home = Path(tempfile.mkdtemp(dir="/var/tmp"))  # not /tmp: the script treats /tmp trust as stale
    try:
        check(home)
    finally:
        shutil.rmtree(home)


def check(home: Path) -> None:
    releases = home / ".codex/packages/standalone/releases"
    for version in ["1.0", "1.1", "1.2", "1.3"]:
        make(releases / version, 40, folder=True)
    (home / ".codex/packages/standalone/current").symlink_to(releases / "1.0")
    old_log = make(home / ".codex/archived_logs/old.log", 20)
    fresh_log = make(home / ".codex/archived_logs/fresh.log", 0.1)
    live_db = make(home / ".codex/archived_logs/state.sqlite-wal", 20)
    old_chat = make(home / ".codex/archived_sessions/chat.jsonl", 45)
    (home / "Workspaces/kept").mkdir(parents=True)
    (home / ".codex/config.toml").write_text(
        f'model = "m"\n\n[projects."{home}/Workspaces/kept"]\ntrust_level = "trusted"\n\n'
        f'[projects."{home}/gone"]\ntrust_level = "trusted"\n\n[projects."/tmp"]\ntrust_level = "trusted"\n\n'
        '[tui]\nnotifications = ["x"]\n')

    found = {c.path for c in cleanup.candidates(home, time.time(), set())}
    # Active version (1.0) and newest two (1.2, 1.3) are kept; only 1.1 goes.
    assert {p for p in found if p.parent == releases} == {releases / "1.1"}, found
    assert old_log in found and old_chat in found
    assert fresh_log not in found, "items newer than a day must be skipped"
    assert live_db not in found, "live database files must never be candidates"

    busy = cleanup.candidates(home, time.time(), {str(old_log)})
    assert all(c.blocked for c in busy if c.path == old_log), "open files must block deletion"

    subprocess.run([sys.executable, SCRIPT, "--home", home, "--apply", "rebuildable"], check=True, capture_output=True)
    assert not old_log.exists() and not (releases / "1.1").exists()
    assert old_chat.exists(), "--apply rebuildable must leave history alone"
    assert (releases / "1.0").exists() and fresh_log.exists() and live_db.exists()

    subprocess.run([sys.executable, SCRIPT, "--home", home, "--fix-config"], check=True, capture_output=True)
    config = tomllib.loads((home / ".codex/config.toml").read_text())
    assert list(config["projects"]) == [f"{home}/Workspaces/kept"], config["projects"]
    assert config["tui"] == {"notifications": ["x"]} and config["model"] == "m"
    print("agent-home-cleanup checks passed")


if __name__ == "__main__":
    main()
