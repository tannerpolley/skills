---
name: t3-code
description: Map of T3 Code's host tools for work on threads rather than code. Use inside T3 Code (t3_* or mcp__t3-code__* tools present) to pick a model for delegate_task; read, message, or wait on another thread, including one in another project; answer a delegated child's question; edit a thread's message queue; fork or merge back; rename, pin, snooze, or archive a thread; send a file; or move this thread into a worktree.
---

# T3 Code tools

The T3 Code orchestration instructions already in your context own delegation, launching new threads, scheduling, worktree launches, and PR linking. This skill covers the rest. Tools may be deferred: load a tool's schema by name (in Claude Code, `ToolSearch` with `select:<name>`) before calling it, and read its description, which is authoritative for parameters.

## Subagent models

The model tiers come from the global rules; these are their `delegate_task` targets. Check `orchestrator_capabilities` if one is rejected.

| Use | `target` |
|---|---|
| Main worker: implementation, fixes, tests; also budget review, sanity checks, managing | `{"providerInstanceId":"codex","model":"gpt-6.1-sol","options":{"reasoningEffort":"high"}}` |
| The hardest implementation pieces (Opus 5.5 orchestrates by default) | `{"providerInstanceId":"claudeAgent","model":"claude-opus-5-5","options":{"effort":"high"}}` |
| Exploration, searches, reading, diagnosis probes (not implementation) | `{"providerInstanceId":"codex","model":"gpt-6-luna","options":{"reasoningEffort":"max"}}` |
| Quick, well-specified Claude-side work | `{"providerInstanceId":"claudeAgent","model":"claude-sonnet-5-5","options":{"effort":"medium"}}` |
| Strong review, or guidance for an Opus 5.5 orchestrator | `{"providerInstanceId":"codex","model":"gpt-6-astra","options":{"reasoningEffort":"xhigh"}}` |

Codex agents can run these natively instead; Claude agents need `delegate_task`. Give an advisor the question, the evidence, and what you already ruled out, and treat its answer as input to your decision.

## Another thread (not your delegated child)

- Find it: `t3_thread_list` covers only this project; `t3_thread_search` also covers other projects when the user allows it.
- Read it with `t3_thread_read`, paging on `nextPosition`. `t3_thread_wait` reports status only; its timeout leaves the run going.
- Message it with `t3_thread_send`: `auto` starts, steers, or queues as fits; `queue` for a separate follow-up, `steer` to update the running turn, `restart` to interrupt and restart it. Pass a stable `clientRequestId` so a retry cannot send twice.
- Its reply never wakes you. Wait on or read the thread to get it.
- Stop a turn with `t3_thread_interrupt`.

Other projects: a top-level thread can read them when the user turned on "Top-level threads can read other projects" in Settings → Customizations, and can also send to them with "Top-level threads can prompt other projects". Subagents and delegated tasks stay in their own project. A `thread_not_found` naming Settings → Customizations means the switch is off: tell the user which switch to turn on.

Every write keeps the permission ceiling: you cannot drive a thread with broader runtime or interaction modes than your own.

## Your delegated children

- Pass `workspace: "worktree"` to `delegate_task` when a child edits code in parallel with you or its siblings: it gets its own worktree on a new branch from yours. Keep research and review children on the default. Its commits stay on its branch until you merge or cherry-pick them.
- A child's completion wakes you. End your turn instead of polling; call `task_status` only when you need the result mid-turn.
- Sending a child more work with `t3_thread_send` reopens its task, and that turn's result wakes you too unless the user turned that off (then read `task_status`).
- `waitingOnUser` means the child is blocked on the user. Answer a question with `t3_pending_request_respond` on the child's thread (find it with `t3_pending_request_list` / `t3_pending_request_read`). Permission approvals are the user's to grant: relay them.
- Report each child's `taskId` or thread ID to the user; say work is running only when a tool confirmed it.

## A thread's queue

`t3_queue_list` shows queued messages in delivery order. `t3_queue_edit` rewrites one, `t3_queue_reorder` moves it (`beforeRunId: null` for the end), `t3_queue_cancel` drops it, and `t3_queue_promote_to_steer` delivers it into the active run now.

## Forks and merge-back

`t3_thread_fork` branches this thread from a run or checkpoint to try an alternative. `t3_thread_merge_back` carries this thread's context back to a related thread in the same project; `t3_thread_transfers` shows how that transfer is going. Acceptance means recorded, not that a provider turn finished.

## Housekeeping

- `t3_thread_update` renames a thread, regenerates its title, or links and unlinks a PR.
- `t3_thread_organize` pins, snoozes (with `snoozedUntil`), settles, archives, or marks a thread unread.
- `t3_thread_configuration` reads a thread's model and modes; `t3_thread_configure` changes this thread's own provider and model; `orchestrator_capabilities` lists the choices.
- `t3_environment_read` and `t3_environment_preferences_update` read and change environment-wide preferences, including custom instructions (4,000 characters at most). Change them only when the user asks.

## Files

`t3_attachment_prepare_upload` returns a signed URL; POST the exact bytes to it, then `t3_thread_send_attachments`. Each send is a new message with no retry key, so after an uncertain failure read the thread before sending again. `t3_attachment_discard` drops an unsent upload.

## Moving this thread into a worktree

Check `t3_worktree_status` first. `t3_worktree_handoff` ends the current turn, so make it the turn's last call and pass the remaining work as `continuationPrompt`. To start a separate thread in a worktree instead, use `t3_thread_launch` as the orchestration instructions describe.
