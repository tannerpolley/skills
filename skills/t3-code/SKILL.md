---
name: t3-code
description: Map of T3 Code's host tools for work on threads rather than code. Use inside T3 Code (t3_* or mcp__t3-code__* tools present) to pick a model for delegate_task; read, message, or wait on another thread, including one in another project; answer a delegated child's question; edit a thread's message queue; fork or merge back; rename, pin, snooze, or archive a thread; send a file; or move this thread into a worktree.
---

# T3 Code tools

The T3 Code orchestration instructions already in your context own delegation, launching new threads, scheduling, worktree launches, issues, and PR linking. This skill maps the rest. Tools may be deferred: load a tool's schema by name (in Claude Code, `ToolSearch` with `select:<name>`) before calling it. Its description is authoritative for parameters and wins over this skill.

## Picking a model

`orchestrator_capabilities` lists the model roles the user set in Settings → Customizations (orchestrator, implementor, checker, reviewer, investigator, designer), each with its `target` JSON, availability and weekly headroom. Read it before delegating and pass a role's target as `delegate_task`'s `target`. Never hard-code a model here or in a brief; the roles change.

## Another thread (not your delegated child)

- Find it: `t3_thread_list` covers this project; `t3_thread_search` searches titles, branches, PRs and message text, across projects when allowed.
- Read it with `t3_thread_read`, keeping `limit` and `maxCharsPerItem` small and paging with `afterPosition=nextPosition`. `t3_thread_wait` reports status only; its timeout leaves the run going.
- Message it with `t3_thread_send`: `auto` starts, steers, or queues as fits; `queue` for a separate follow-up, `steer` to update the running turn, `restart` to interrupt and restart it. Pass a stable `clientRequestId` so a retry cannot send twice.
- Its reply never wakes you. Wait on or read the thread to get it.
- Stop a turn with `t3_thread_interrupt`.

Other projects: a top-level thread can read them when the user turned on "Top-level threads can read other projects" in Settings → Customizations, and can send to them with "Top-level threads can prompt other projects". Subagents and delegated tasks stay in their own project. A `thread_not_found` naming Settings → Customizations means the switch is off: tell the user which switch to turn on.

Every write keeps the permission ceiling: you cannot drive a thread with broader runtime or interaction modes than your own.

## Your delegated children

- A child's completion wakes you. End your turn instead of polling; call `task_status` only to read a finished result.
- Sending a finished child more work with `t3_thread_send` starts a fresh task (it returns the new `taskId`), and that result wakes you too.
- A child blocked on a question: `t3_pending_request` with `list` or `read` on the child's thread, then `respond` with `answers`. Approvals (`decision`) only for delegated descendants within your authority; otherwise relay them to the user.
- Stop a child with `task_cancel`.
- Report each child's thread link to the user; say work is running only when a tool confirmed it.

## A thread's queue

`t3_queue` (omit `threadId` for this thread): `list` in send order, `read` one, `edit` its text, `cancel` it, `reorder` before `beforeRunId` (null for the end), or `promote_to_steer` to deliver it into the active run now.

## Forks and merge-back

`t3_thread_transfer`: `fork` copies a thread from a run or checkpoint into a new thread to try an alternative; `merge_back` carries this thread's context into a related thread in the same project; `status` shows how a transfer is going. Acceptance means recorded, not that a provider turn finished.

## Housekeeping

- `t3_thread_update` renames a thread or regenerates its title. PR links use `link_pull_request` / `unlink_pull_request`.
- `t3_thread_organize` pins, snoozes (with `snoozedUntil`), settles, archives, or marks a thread unread, and undoes each.
- `t3_thread_configure` reads a thread's model and modes, or sets its model with `modelSelection` from `orchestrator_capabilities`.
- `t3_environment_read` and `t3_environment_preferences_update` read and change environment-wide preferences, including custom instructions. Change them only when the user asks.

## Files

`t3_attachment_prepare_upload` returns a signed URL; POST the exact bytes to it, then `t3_thread_send_attachments`. Each send is a new message with no retry key, so after an uncertain failure read the thread before sending again. `t3_attachment_discard` drops an unsent upload.

## Moving this thread into a worktree

Check `t3_worktree_status` first. `t3_worktree_handoff` ends the live session, so make it the turn's last call and pass the remaining work as `continuationPrompt`. `t3_worktree_return_to_root` moves back to the main checkout the same way. To start a separate thread in a worktree instead, use `t3_thread_launch` as the orchestration instructions describe.
