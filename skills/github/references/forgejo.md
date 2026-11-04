# Forgejo repositories

Since 2026-11-02 the owner's repositories live on Forgejo at `tnnrpolley21-ms-7c95.taila72856.ts.net:3000`. A checkout is a Forgejo repository when `git remote get-url origin` points at that host. Its GitHub namesake is a one-way copy kept by a desktop timer: never open pull requests, write issues or push there, because the copy overwrites GitHub edits. Third-party clones whose `origin` is GitHub stay GitHub repositories.

Use `fj` (Forgejo CLI, already signed in) or the Forgejo API, not `gh`. Pass `-H tnnrpolley21-ms-7c95.taila72856.ts.net:3000` on every `fj` command. `fj` stores its token in `~/.local/share/forgejo-cli/keys.json`; read it for API calls and never print it.

## Issues

Inside T3 Code, write issues through T3's tools (`t3_issue_post`, `propose_issue_change`) with the Forgejo host, so the Issues pane and orchestration see them. Outside T3, use `fj issue create|comment|close`. Forgejo has no sub-issues: T3 writes `Part of #N` in the child body. Blockers are Forgejo issue dependencies (`fj issue depend`).

## Pull requests

- Open: push the branch to `origin`, then `fj -H <host> pr create --base main --head <branch> --body "… Closes #N …" "<title>"`.
- Merge on Forgejo, not by pushing `main`: `fj -H <host> pr merge <n> -M fast-forward-only -d`, or `-M rebase -d` when `main` moved. This keeps `main` linear, marks the pull request merged and deletes its branch. Then update local `main` with `git fetch` and `git merge --ff-only origin/main`, without switching a checkout another task occupies.
- Pushing `main` and deleting the branch yourself closes the pull request as unmerged: Forgejo checks for the merge after the push and finds the branch gone. The `forgejo-merge-repair` timer marks such pull requests merged within 5 minutes, but do not rely on it.
- Forgejo does not close the issues a pull request names when it detects a pushed merge; T3 closes them for linked threads. Verify closure after merge and close by hand if needed.
