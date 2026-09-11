# Worker transports

Read this reference whenever the manager staffs, dispatches, replaces, or receives a worker.

## Choose with the user

Transport controls lifecycle and isolation; model and effort control capability and cost. Present only currently callable combinations, recommend one with a short reason, and obtain the user's choice through native input before dispatch.

- **App task:** Prefer for difficult or long-running work, cross-turn continuity, direct user steering, or a dedicated Codex worktree. Luna fits clear bounded work; Sol or Astra fits harder, ambiguous, or larger work.
- **Native subagent:** Prefer for small or well-specified work and bounded research, testing, or implementation that should return directly to its parent. Luna is the economical default; choose a stronger supported model when the assignment needs it.
- **CSE-Pi:** Prefer for scientific work needing a frozen work order, sandboxed candidate, structured termination, and retained evidence. Select any supported model and effort by task difficulty; the guardrails do not depend on model tier.

Keep one numbered baton, assignment, correction count, and current holder across transport or model changes.

## App task

Create the worker in the recorded project and selected local or worktree environment. Record only the exact returned task ID. The worker writes its result, sets the manager as holder, sends the routing line from the main skill exactly once, and stops after successful delivery. The sender makes no receipt read or wait call.

## Native subagent

Spawn a direct child with the selected model, effort, assignment, baton path, and exact return format; record only the exact returned subagent ID. A child may receive later corrections while it remains an active direct child of the same parent and the live tool supports follow-up input. A closed child or a different parent session requires a fresh subagent.

For a batch, spawn all independent children, request one consolidated terminal return, then yield completely to native orchestration. If the live tool requires an explicit barrier, call it once with the complete child-ID set. Do no other model work, status narration, `wait_threads`, thread reads, repeated barrier calls, or child-status/log polling while the batch runs. Codex's native aggregation is the collector; add an evidence-lead child only when synthesis is substantial and nested delegation is callable.

On the terminal return, verify the child's identity and result, write or retain its result artifact, and set the manager as holder. The child does not send an app-task receipt.

## CSE-Pi

Use only a verified CSE-Pi launcher and supported model configuration. Freeze the work order, source identity, paths, non-goals, acceptance, validation, parent identity, budget, and output directory before launch. Register its work-order task ID as holder, budget the run to fit one supported blocking wait, and record the returned run identity. Run it once in the foreground; do not start a daemon, goal, watcher, or short polling loop. If one blocking wait cannot cover the run, recommend another transport instead.

Verify the terminal status, `result.json`, result hash, retained evidence, and candidate or analysis outputs before setting the manager as holder. `needs_parent_input` returns the same baton for clarification; a later CSE-Pi attempt is a new one-shot run with the inherited correction history. The manager alone applies accepted candidate changes.
