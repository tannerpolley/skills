# Worker transports

Read this reference whenever the manager staffs, dispatches, replaces, or receives a worker.

## Choose with the user

Transport controls lifecycle and isolation; model and effort control capability and cost. A worker may use any callable model and supported reasoning effort on any transport. Luna is the default model; the manager selects its effort and recommends another model only when the fully explicit assignment remains demanding. A precise, bounded plan favors Luna; difficult diagnosis, mathematics, broad integration, or high-risk verification may justify more capability. A plan gap requires clarification rather than a stronger worker. Present only currently callable combinations, recommend one with a short reason, and obtain the user's choice through native input before dispatch.

- **App task:** Prefer for difficult or long-running work, cross-turn continuity, direct user steering, or a dedicated Codex worktree.
- **Native subagent:** Prefer for small or well-specified work and bounded research, testing, or implementation that should return directly to its parent.
- **CSE-Pi:** Prefer for scientific work needing a frozen work order, sandboxed candidate, structured termination, and retained evidence; its guardrails do not depend on model tier.

Keep one numbered baton, assignment, correction count, and current holder across transport or model changes.

## App task

Create the worker in the recorded project and selected local or worktree environment. Record only the exact returned task ID. The worker writes its result, sets the manager as holder, sends the routing line from the main skill exactly once, and stops after successful delivery. The sender makes no receipt read or wait call.

## Native subagent

Spawn one direct child by default with the selected model, effort, numbered assignment, pointers to only the needed brief or plan sections, and exact return format; record only the exact returned subagent ID. Do not copy the Baton protocol or unrelated session material into its prompt. A child may receive later corrections while it remains an active direct child of the same parent and the live tool supports follow-up input. A closed child or a different parent session requires a fresh subagent.

Use concurrent children only when the live tool contract explicitly guarantees one barrier returns the complete child set. Spawn that set, call the barrier once with every child ID, and yield completely. Without that guarantee, keep one native child or select app-task or CSE-Pi workers for parallel assignments. Do no other model work, status narration, `wait_threads`, thread reads, repeated barrier calls, or child-status/log polling while delegated work runs.

On the terminal return, verify the child's identity and result, write or retain its result artifact, and set the manager as holder. The child does not send an app-task receipt.

## CSE-Pi

Use only a verified CSE-Pi launcher and supported model configuration. Write the selected model and effort into its frozen work order so Baton staffing does not depend on runtime role defaults. Freeze the source identity, paths, non-goals, acceptance, validation, parent identity, budget, and output directory before launch. Register its work-order task ID as holder, budget model turns for the expected tool round-trips and the run to fit one supported blocking wait, then record the returned run identity. Run it once in the foreground; do not start a daemon, goal, watcher, or short polling loop. If one blocking wait cannot cover the run, recommend another transport instead.

Verify the terminal status, `result.json`, result hash, retained evidence, and candidate or analysis outputs before setting the manager as holder. `needs_parent_input` returns the same baton for clarification; a later CSE-Pi attempt is a new one-shot run with the inherited correction history. The manager alone applies accepted candidate changes.
