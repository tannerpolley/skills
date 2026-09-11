---
name: baton-pass
description: Coordinate an explicitly selected Baton Pass workflow through architect, manager, worker, and independent review, preserving its planning and staffing gates.
---

# Baton Pass

Run one cooperative delivery workflow in the repository's saved local checkout. Use native Codex task and collaboration tools directly.

Before planning or review disposition, read [shared review recovery](/home/tnnrpolley21/.codex/references/review-control.md). Keep acceptance, finding dispositions, and correction history in the existing brief and handoffs.

## Hard boundary

Run only during active user turns. Never create or use automations, scheduled tasks, heartbeats, cron, timers, delayed wakeups, background watchers, or `wait_threads`. Treat a successful `send_message_to_thread` result naming the exact registered recipient as the sole delivery acknowledgement. Make no post-send `read_thread`, wait, or monitoring call and do not roll back the holder after that success. Proceed only to the next already-authorized handoff in a parallel dispatch batch; otherwise stop. Later progress arrives through a return baton or a new user turn. If CI or another external condition is still pending, report it and wait for a new user message.

## Start

1. Inspect the saved project and repository without changing them. Confirm that the task is substantial enough to benefit from architect, manager, worker, and independent-review roles.
2. Verify the required app-task and native-reviewer tools are callable. Resolve the initiating task's exact saved `projectId`; every persistent architect, manager, or worker task must use that same recorded project ID, including reused tasks. The architect role has planning and advisory duties; one task may own either or both, but both duties need a registered owner before worker implementation starts. Default to one architect owning both. Recommend available models and supported reasoning efforts for the architect assignment, with short reasons. Use native input to settle that staffing, any duty split, and optional Fable review, reusing choices already established. Report an unavailable capability or project mismatch before creating or messaging tasks; app tasks and native children are distinct.
3. After confirmation, require a clean GitHub-backed saved local checkout. Fix the role topology: the calling task is the coordinator unless the user explicitly makes it the manager; never create a second manager. Create `docs/baton-pass/<session-id>/`, add `/docs/baton-pass/` only to the checkout's local `.git/info/exclude`, and write `brief.md` plus a small `status.md` containing the session, repository, recorded project ID, topology, architect duty owners, execution mode, numbered batons and holders, and role task IDs.
4. Create one fresh architect app task owning planning and any approved advisory duty with the recorded `projectId`, `environment: {type: "local"}`, the confirmed model and effort, and a prompt containing the session path, task brief, duties, baton 0, and exact next handoff from [Handoffs](#handoffs). Do not create an advisory-only architect, manager, or worker yet.

If task creation or a direct message has an ambiguous result, stop and show the user the known facts. Never retry automatically or create a replacement task without the user's direction.

## Architect

The architect is repository-read-only except for the ignored session folder. Planning duty owns initial research and design; advisory duty owns later design questions and plan-fidelity review. One architect task owns both by default, or separate architect tasks may own one duty each as recorded in `status.md`.

When assigned planning duty:

1. Read the brief, repository instructions, relevant code, tests, and issue or specification.
2. Write `plan.md` with authorized outcomes/phases, non-goals, implementation approach, observable acceptance, material ownership decisions, important risks, and verification. Identify any genuinely independent, non-overlapping worker assignments and their expected paths and dependencies; keep optional experiments and future phases distinct from authorized implementation.
3. Choose any currently available model and supported reasoning effort for manager and each candidate worker assignment. Explain what each assignment needs and why that model/effort fits. Role names do not imply model families.
4. When `status.md` already names the calling task as manager, set it as holder of baton 0, send it the `plan-ready` handoff, and stop. The manager asks the user to approve or revise the plan and staffing together, selects execution mode as described below, then creates the worker task or tasks and, only for an approved duty split, the advisory architect.
5. Otherwise ask the user to approve or revise the plan and staffing together. After approval, create the fresh manager app task and, only for an approved duty split, one advisory architect app task, all with the same recorded project ID and `environment: {type: "local"}` using the approved combinations. Give each an inert setup prompt naming its role, architect duties if applicable, session path, and exact next handoff. The manager creates every worker after selecting execution mode.
6. Record their task IDs and architect duty owners in `status.md`, set manager as holder of baton 0, send the manager the `plan-ready` handoff, and stop.

When assigned advisory duty, act only on a manager handoff. For `design-question`, research only as needed, resolve the stated gap in `plan.md`, and return the same implementation baton as `clarification-ready` to the manager. Obtain user approval before changing an accepted outcome, non-goal, architecture or ownership decision, or acceptance criterion. For plan-fidelity review on baton 0, compare the local candidate with `brief.md` and `plan.md`, including the root no-overengineering rule. Reject bandaid layers that retain the diagnosed broken implementation. Return `PASS` or one consolidated findings list tied to requirements and evidence, distinguishing blockers from optional advice, then stop.

## Manager

The manager is the only role that mutates Git or GitHub. Enforce the root no-overengineering rule in assignments and acceptance: the only accepted repair removes all broken code within the diagnosed boundary and replaces it with the simplest correct solution. Never dispatch or accept bandaid layers over problematic code; preserve required behavior, safeguards, and unrelated work.

1. Read the approved plan, verify the checkout, reuse or create the task feature branch, and preserve the same outcome, non-goals, acceptance, and correction history in every worker assignment. If plan or staffing approval is still pending, obtain it before worker creation.
2. Use sequential mode with one worker unless the plan exposes a reasonable opportunity for independent, non-overlapping assignments. In sequential mode, create one fresh worker with the recorded project ID, `environment: {type: "local"}`, and approved staffing. When parallelism is reasonable, read [parallel mode](references/parallel-mode.md) and use native input to ask the user to choose sequential or parallel execution; never infer the choice. The manager creates every worker under the selected mode.
3. Create one numbered baton per worker, record each assignment and holder in `status.md`, and send each concise handoff to its exact registered task. Stop after the sequential handoff or complete parallel dispatch batch. Continue only as a numbered baton returns or the user starts a new turn.
4. If a worker returns `clarification-needed`, do no implementation against that baton. Answer only when the accepted plan already resolves it unambiguously; otherwise set the advisory architect as that baton's holder, send a `design-question` handoff with the exact gap and evidence, and stop work on that baton. After `clarification-ready` returns, verify that `plan.md` contains the answer and any material change has user approval, then return the numbered baton with a revised assignment. Other independent batons may continue.
5. When completed work returns, inspect the complete diff and evidence for that numbered baton, including Serena use or its concrete fallback reason for supported code work. Verify that repairs replace the defective implementation at its responsible boundary rather than mask its symptoms. Classify findings before making tiny obvious in-scope replacements or returning that baton to its worker under shared recovery. In parallel mode, integrate returned work only as specified in its reference.
6. After every implementation baton is integrated, run required local checks and commit a coherent combined candidate. Prepare local review evidence: brief, plan, baton assignments, candidate SHA, relevant diff, changed paths, checks, and limitations. A published PR is not a local-review prerequisite.
7. Pass baton 0 to the registered advisory architect for plan-fidelity review. Only manager acceptance and its `PASS` advance the candidate to final review; adjudicate findings against accepted scope before assigning corrections.
8. If the user enabled Fable, use the available `fable-review` skill on a self-contained candidate packet that includes the root no-overengineering requirement. Treat its result as advisory, verify the findings, and ask the user whether to apply or decline them.
9. After manager acceptance and advisory-architect `PASS`, spawn exactly one fresh `gpt-6-astra` native collaboration reviewer at `high` reasoning with no inherited turns, using the live tool schema. Ask for a quick final review limited to the user-approved plan criteria and the root no-overengineering rule. Supply the brief, plan, outcome/non-goals, candidate SHA, diff, checks, and correction history. Require read-only work, no helpers, no Git/GitHub or app-task mutation, and the same no-scheduling boundary. Return `ACCEPT` or a concise list of violated criteria with evidence; optional hardening, new requirements, and reviewer preferences are nonblocking.
10. Adjudicate findings before bounded worker corrections. Renew only invalidated checks or reviews and establish acceptance at the actual final candidate. Preserve correction history across every holder and reviewer.
11. After manager acceptance, advisory-architect `PASS`, selected Fable disposition, and Astra `ACCEPT`, verify publication authority. A local-only endpoint finishes locally; otherwise obtain missing publication authority natively. Immediately before push, verify HEAD, relevant index/worktree state, review evidence, remote target, and existing auto-merge state. A push that could trigger armed auto-merge also needs merge authority.
12. Push only the accepted candidate, create/update the authorized draft PR, and verify its hosted head. Hosted CI and required GitHub reviews that need publication remain merge gates afterward. Any branch update requires renewed affected evidence.
13. Present the exact PR, checks, reviewed head, and merge method. With existing or newly granted merge authority, revalidate the hosted head and request a guarded merge, or enable native auto-merge while hosted gates are pending. Honor existing merge-queue policy without introducing or bypassing one. A head guard is not a permanent lock on later pushes.
14. On observed merge, follow Git and GitHub for exact associated-branch closeout and return the saved checkout to updated local `main`. Pending auto-merge is not a completed merge.

If hosted checks or mergeability are pending, report the actual gate and await an active authorized continuation. Do not poll or schedule a watcher. At a shared recovery trigger, the holder pauses affected edits and returns evidence to the registered manager; the manager must resolve the recovery boundary before another corrective dispatch.

## Worker

The worker writes implementation and tests but does not mutate Git or GitHub. These boundaries apply regardless of worker model.

1. Read only the current numbered assignment, brief, and approved plan. In parallel mode, remain inside the assigned worktree and responsibility boundary.
2. Before implementation and whenever a consequential gap or contradiction appears, verify that the accepted plan and assignment explicitly determine what to build, its responsible boundary, and its acceptance evidence. At the first unresolved gap, stop all implementation on that baton. Do not guess, choose a design, or continue another implementation task. Preserve work already completed, write the exact question and evidence in the session folder, and return the same numbered baton as `clarification-needed` to the manager. The manager either answers from the accepted plan or consults the advisory architect before returning a revised assignment.
3. With no unresolved gap, follow the root no-overengineering rule: never add bandaid code over problematic code. Remove all broken code within the diagnosed boundary and replace it with the simplest correct solution, preserving required behavior, safeguards, and unrelated work. Run proportionate checks against the original failure and affected behavior; if replacement exceeds authority, return the blocker instead of layering a workaround.
4. Write a short result in the session folder with the baton number, changed paths, checks, remaining risk, and inherited correction history. At a recovery trigger, pause affected edits and return the evidence to the manager through the same numbered handoff.
5. Set manager as holder of that baton in `status.md`, then call `mcp__codex_app__send_message_to_thread` exactly once with the manager task ID recorded there and the concise handoff below; only a successful tool result completes the handoff. Create no helper agents or app tasks, and do not commit, switch branches, or integrate work.

## Handoffs

Baton 0 carries planning, staffing, combined review, and delivery. Implementation assignments use batons 1 through N; sequential mode uses only baton 1. Only a baton's holder works on its assignment. The manager may retain baton 0 while workers hold implementation batons and may process multiple returned batons. Every role-creation or follow-up prompt names the exact next handoff that role must perform. A final response reports a completed handoff; it does not replace one.

A handoff is complete only when the sender:

1. writes its required artifact;
2. updates `status.md` with the registered next holder for that baton;
3. receives a successful direct-message result naming that exact registered task; and
4. reports the completed handoff in its final response.

Keep the direct message short:

```text
$baton-pass session=<id> baton=<number> role=<role> action=<action> read=<absolute-session-path>
Completion gate: return a final response only after the required artifact, holder update, and direct message to the exact recorded next task all succeed; otherwise restore yourself as holder of this baton and report the blocker.
```

If the direct message fails, identifies a different task, or has an ambiguous result, restore the sender as holder of that baton, record the failed handoff in `status.md`, report it to the user, and stop. Do not retry or create a replacement task without direction.

If a non-holder receives a manual prompt, it may read `status.md`, identify the current holder of the named baton, and stop without changing repository or workflow state.

This file-based coordination is a convention among trusted tasks, not a security or transaction boundary.

## Finish

Completion means the authorized endpoint and its applicable checks/reviews are satisfied. For an authorized merge endpoint, verify the merge, associated-branch closeout, and saved checkout on updated local `main`, preserving unrelated work. A local-only endpoint does not require publication. Ask whether to retain or delete the ignored session folder. Archive tasks only when the user asks.
