---
name: agent-home-cleanup
description: Report and clear disk space held by local coding-agent homes (Codex, Claude Code, T3 Code, pi) and find config entries pointing at missing paths. Use for agent slowness, disk-space, cleanup, or stale-config requests.
---

# Agent home cleanup

Run `python3 scripts/agent_home_cleanup.py` from this skill directory. It writes nothing and reports:

- agent home sizes;
- **rebuildable** candidates: old agent versions (the active one and the newest two are kept) and logs older than 14 days;
- **history** candidates older than 30 days: archived chats, moved-aside worktrees (may hold uncommitted work), maintenance backups, generated images, and T3 upgrade backups;
- config entries in Codex, Claude Code, and pi settings that point at missing paths.

Large groups are summarized; `--list` shows every path with its exact `rm` command.

## Clearing

- Rebuildable: `--apply rebuildable`. The weekly `agent-home-cleanup.timer` runs this with `--notify`, which also tells the user how much history awaits approval.
- History: show the user the report's history section (sizes, ages, and what each group is), ask with the native question tool, and only after approval run `--apply all`.
- Codex trust entries for missing or `/tmp` folders: `--fix-config`. Fix other missing config paths by hand after checking whether the target moved or was retired.

After applying, give the user the before/after sizes the script prints.

Every candidate must match a rule in `rules()`, be older than a day and its retention, resolve inside its agent home, and hold nothing a running process has open; symlinks and live database files are never candidates. To clear something new, add a rule there instead of deleting by hand. The script never edits agent databases; Codex's Archive button archives chats.
