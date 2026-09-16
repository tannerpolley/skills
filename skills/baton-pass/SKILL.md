---
name: baton-pass
description: Coordinate an explicitly selected Baton Pass workflow through architect, manager, worker, and independent review, preserving its planning and staffing gates.
---

# Baton Pass

Run one cooperative delivery workflow in one repository and its recorded project. Cross-repository delivery requires a separate Baton Pass session and manager for each repository. Use native Codex task and subagent tools.

Before planning or review disposition, read [shared review recovery](/home/tnnrpolley21/.codex/references/review-control.md). Keep acceptance, finding dispositions, and correction history in the existing plan, role artifacts, and handoffs.

## Hard boundary

Bind the workflow to the initiating task's exact in-app `projectId`. The initiating task and every persistent architect, manager, reviewer, and app-task worker must belong to that same project; native subagents must be direct children of a project-bound participant. Never create or reuse a projectless task or a task from another project. If the initiating task has no project or any participant cannot be verified against the recorded project ID, stop before creating or messaging roles and ask the user to continue from the intended project.

Run only during active user turns and use event-return coordination. Default to one native subagent and yield completely until its terminal result. Use concurrent native children only when the live tool contract explicitly guarantees one wait returns the complete set; otherwise choose app-task workers for parallel assignments. An app-task sender treats a successful `send_message_to_thread` result naming the exact registered recipient as the sole delivery acknowledgement and stops. Never create or use automations, scheduled tasks, heartbeats, cron, timers, delayed wakeups, background watchers, goals, `wait_threads`, repeated native-agent waits, status reads, log reads, or progress prompts to monitor delegated work. Make no post-send `read_thread` call and do not roll back the holder after successful delivery. Later progress arrives through a return baton or a new user turn. If CI or another external condition is still pending, report it and wait for a new user message.

This loaded skill is the sole authority for workflow and handoff mechanics. Session files own task-specific scope, evidence, and current state only; never copy protocol rules into them. If stale session text conflicts with this skill, follow this skill and report the stale text to the manager.

## Start

1. Inspect the saved project and repository without changing them. Confirm that the task is substantial enough to benefit from architect, manager, worker, and independent-review roles.
2. Inventory callable app-task, native-subagent, and native-reviewer tools; unavailable optional worker transports do not block the workflow. Verify the initiating task and every reused participant against the exact saved `projectId`. Record task and subagent IDs only from successful tool results; never infer or transcribe them from prose. The architect role has planning and advisory duties; one task may own either or both, but both duties need a registered owner before worker implementation starts. Default to one architect owning both. Recommend available models and supported reasoning efforts for the architect assignment, with short reasons. Use native input to settle that staffing, any duty split, optional read-only research delegation, and optional Fable review, reusing choices already established. Report an unavailable required capability or project mismatch before creating or messaging tasks; app tasks and native children are distinct.
3. After confirmation, require a clean GitHub-backed saved local checkout. Fix the role topology: the calling task is the coordinator unless the user explicitly makes it the manager; never create a second manager. Create `docs/baton-pass/<session-id>/`, add `/docs/baton-pass/` only to the checkout's local `.git/info/exclude`, and write `brief.md`, a compact current-state `status.md`, and `baton-control.md`. Keep history in role artifacts; `status.md` contains only session, repository, project ID, topology, exact architect and manager task IDs, architect duty owners, execution mode, and baton-file index.
4. Create one fresh architect app task owning planning and any approved advisory duty with the recorded `projectId`, `environment: {type: "local"}`, the confirmed model and effort, and a prompt containing the session path, task brief, duties, control baton, and exact next handoff from [Handoffs](#handoffs). Record the returned ID and set the architect as holder in `baton-control.md`. Do not create an advisory-only architect, manager, or worker yet.

If task creation or a direct message has an ambiguous result, stop and show the user the known facts. Never retry automatically or create a replacement task without the user's direction.

## Architect

The architect is repository-read-only except for the ignored session folder. Planning duty owns initial research and design; advisory duty owns later design questions and plan-fidelity review. One architect task owns both by default, or separate architect tasks may own one duty each as recorded in `status.md`.

For approved research or retrieval, the architect may dispatch one fresh read-only Luna subagent at low or medium effort with the complete bounded question. Multiple children require a live wait-all guarantee; otherwise use one evidence-lead child to gather and synthesize the packet itself. After dispatch, the architect yields completely and does not monitor or narrate progress.

When assigned planning duty:

1. Read the brief, repository instructions, relevant code, tests, and issue or specification.
2. Write `plan.md` with authorized outcomes/phases, non-goals, implementation approach, observable acceptance, material ownership decisions, important risks, and verification. Identify any genuinely independent, non-overlapping worker assignments and their expected paths and dependencies; keep optional experiments and future phases distinct from authorized implementation.
3. Choose any currently available model and supported reasoning effort for the manager and recommend a worker transport, model, and effort for each candidate assignment. Explain the plan's explicitness plus the difficulty, duration, isolation, and evidence needs behind each recommendation. Role names do not imply model families.
4. When `status.md` already names the calling task as manager, set it as holder in `baton-control.md`, send it the `plan-ready` handoff, and stop. The manager asks the user to approve or revise the plan and staffing together, selects execution mode as described below, then creates the worker task or tasks and, only for an approved duty split, the advisory architect.
5. Otherwise ask the user to approve or revise the plan and staffing together. After approval, create the fresh manager app task and, only for an approved duty split, one advisory architect app task, all with the same recorded project ID and `environment: {type: "local"}` using the approved combinations. Give each an inert setup prompt naming its role, architect duties if applicable, session path, and exact next handoff. The manager creates every worker after selecting execution mode.
6. Record their exact returned task IDs and architect duty owners in `status.md`, set manager as holder in `baton-control.md`, send the manager the `plan-ready` handoff, and stop.

When assigned advisory duty, act only on a manager handoff. For `design-question`, research only as needed, resolve the stated gap in `plan.md`, and return the same implementation baton as `clarification-ready` to the manager. Obtain user approval before changing an accepted outcome, non-goal, architecture or ownership decision, or acceptance criterion. For plan-fidelity review on the control baton, compare the local candidate with `brief.md` and `plan.md`, including the root no-overengineering rule. Reject bandaid layers that retain the diagnosed broken implementation. Return `PASS` or one consolidated findings list tied to requirements and evidence, distinguishing blockers from optional advice, then stop.

## Manager

The manager is the only role that mutates Git or GitHub. Enforce the root no-overengineering rule in assignments and acceptance: the only accepted repair removes all broken code within the diagnosed boundary and replaces it with the simplest correct solution. Never dispatch or accept bandaid layers over problematic code; preserve required behavior, safeguards, and unrelated work. Before every corrective dispatch, read and increment that baton's correction-round count. If the dispatch would begin a third round, follow shared review recovery instead of sending it.

At that recovery boundary, when evidence shows worker capability rather than a plan or design gap is the blocker, the manager uses native input to recommend either one fresh worker on a stronger available model or transport, such as Sol or Astra in an app task, or manager completion of the bounded remainder. State the failed acceptance evidence, attempt history, preserved work, and reason for the recommendation; wait for confirmation before creating the replacement or implementing. Keep the same numbered baton, assignment, and correction count without overlapping holders or resetting attempts. User-confirmed manager completion authorizes that bounded exception to worker implementation ownership.

1. Read the approved plan, verify the checkout, reuse or create the task feature branch, and preserve the same outcome, non-goals, acceptance, and correction history in every worker assignment. Worker assignments contain implementation only; route research, planning, and design through the architect. If plan or staffing approval is still pending, obtain it before worker creation.
2. Read [worker transports](references/worker-transports.md). Present only callable transport, model, and effort combinations, recommend one for each assignment, and use native input to ask the user to choose. Ask for sequential or parallel execution in the same decision when the plan exposes independent, non-overlapping assignments; never infer either choice.
3. Create one `baton-<number>.md` per worker containing its assignment, selected transport, manager as holder, state, and correction-round count; add only its path to the `status.md` index. Dispatch through the selected transport, then record the exact returned worker identity and transfer the baton as specified in its reference. Stop or yield after the sequential handoff or complete parallel dispatch batch as required by that transport. Continue only as a numbered baton returns or the user starts a new turn.
4. If a worker returns `clarification-needed`, do no implementation against that baton. Answer only when the accepted plan already resolves it unambiguously; otherwise set the advisory architect as that baton's holder, send a `design-question` handoff with the exact gap and evidence, and stop work on that baton. After `clarification-ready` returns, verify that `plan.md` contains the answer and any material change has user approval, then return the numbered baton with a revised assignment. Other independent batons may continue.
5. When completed work returns, inspect the complete diff and evidence for that numbered baton, including Serena use or its concrete fallback reason for supported code work. Verify that repairs replace the defective implementation at its responsible boundary rather than mask its symptoms. Classify findings before making tiny obvious in-scope replacements or returning that baton to its worker under shared recovery. In parallel mode, integrate returned work only as specified in its reference.
6. After every implementation baton is integrated, run required local checks and commit a coherent combined candidate. Prepare local review evidence: brief, plan, baton assignments, candidate SHA, relevant diff, changed paths, checks, and limitations. A published PR is not a local-review prerequisite.
7. Pass the control baton to the registered advisory architect for plan-fidelity review. Only manager acceptance and its `PASS` advance the candidate to final review; adjudicate findings against accepted scope before assigning corrections.
8. If the user enabled Fable, use the available `fable-review` skill on a self-contained candidate packet that includes the root no-overengineering requirement. Treat its result as advisory, verify the findings, and ask the user whether to apply or decline them.
9. After manager acceptance and advisory-architect `PASS`, spawn exactly one fresh `gpt-6-astra` native collaboration reviewer at `high` reasoning with no inherited turns, using the live tool schema. Ask for a quick final review limited to the user-approved plan criteria and the root no-overengineering rule. Supply the brief, plan, outcome/non-goals, candidate SHA, diff, checks, and correction history. Require read-only work, no helpers, no Git/GitHub or app-task mutation, and the same no-scheduling boundary. Return `ACCEPT` or a concise list of violated criteria with evidence; optional hardening, new requirements, and reviewer preferences are nonblocking.
10. Adjudicate findings before bounded worker corrections. Renew only invalidated checks or reviews and establish acceptance at the actual final candidate. Preserve correction history across every holder and reviewer.
11. After manager acceptance, advisory-architect `PASS`, selected Fable disposition, and Astra `ACCEPT`, verify publication authority. A local-only endpoint finishes locally; otherwise obtain missing publication authority natively. Immediately before push, verify HEAD, relevant index/worktree state, review evidence, remote target, and existing auto-merge state. A push that could trigger armed auto-merge also needs merge authority.
12. Push only the accepted candidate, create/update the authorized draft PR, and verify its hosted head. Hosted CI and required GitHub reviews that need publication remain merge gates afterward. Any branch update requires renewed affected evidence.
13. Present the exact PR, checks, reviewed head, and merge method. With existing or newly granted merge authority, revalidate the hosted head and request a guarded merge, or enable native auto-merge while hosted gates are pending. Honor existing merge-queue policy without introducing or bypassing one. A head guard is not a permanent lock on later pushes.
14. On observed merge, follow Git and GitHub for exact associated-branch closeout and return the saved checkout to updated local `main`. Pending auto-merge is not a completed merge.

If hosted checks or mergeability are pending, report the actual gate and await an active authorized continuation. Do not poll or schedule a watcher. At a shared recovery trigger, the holder pauses affected edits and returns evidence to the registered manager; the manager must resolve the recovery boundary before another corrective dispatch.

## Worker

The worker writes implementation and tests but does not mutate Git or GitHub. It may run as an app task or native subagent; these boundaries apply regardless of transport or model.

1. Read only the current numbered assignment, brief, and approved plan. Treat any research, planning, or design assignment as an unresolved gap and return it without implementation. In parallel mode, remain inside the assigned worktree and responsibility boundary.
2. Before implementation and whenever a consequential gap or contradiction appears, verify that the accepted plan and assignment explicitly determine what to build, its responsible boundary, and its acceptance evidence. At the first unresolved gap, stop all implementation on that baton. Do not guess, choose a design, or continue another implementation task. Preserve work already completed, write the exact question and evidence in the session folder, and return the same numbered baton as `clarification-needed` to the manager. The manager either answers from the accepted plan or consults the advisory architect before returning a revised assignment.
3. With no unresolved gap, follow the root no-overengineering rule: never add bandaid code over problematic code. Remove all broken code within the diagnosed boundary and replace it with the simplest correct solution, preserving required behavior, safeguards, and unrelated work. Run proportionate checks against the original failure and affected behavior; if replacement exceeds authority, return the blocker instead of layering a workaround.
4. Write a short result in the session folder with the baton number, changed paths, checks, remaining risk, and inherited correction history, or return the equivalent structured result for the manager to retain. At a recovery trigger, pause affected edits and return the evidence to the manager through the same numbered handoff.
5. Return the result through the selected completion contract in [worker transports](references/worker-transports.md). Create no helpers, and do not commit, switch branches, or integrate work.

## Handoffs

The control baton carries planning, staffing, combined review, and delivery. Implementation assignments use numbered batons 1 through N; sequential mode uses only baton 1. Only a baton's holder works on its assignment. The manager may retain the control baton while workers hold implementation batons and may process multiple returned batons. Every role-creation or follow-up prompt names the exact next handoff that role must perform. A final response reports a completed handoff; it does not replace one.

An app-task handoff is complete only when the sender:

1. writes its required artifact;
2. updates that baton's file with the registered next holder;
3. receives a successful direct-message result naming that exact registered task; and
4. reports the completed handoff in its final response.

Keep the direct message to this routing line; do not copy completion mechanics into prompts or session artifacts:

```text
$baton-pass session=<id> baton=<control-or-number> from=<sender-role> to=<recipient-role> action=<action> read=<absolute-session-path>
```

If the direct message fails, identifies a different task, or has an ambiguous result, restore the sender as holder in that baton's file, record the failure in the sender's role artifact, report it to the user, and stop. Do not retry or create a replacement task without direction.

Native-subagent worker returns use [worker transports](references/worker-transports.md); the manager updates the holder only after receiving and verifying the terminal result. They do not send app-task receipt messages.

If a non-holder receives a manual prompt, it may read the named baton file, identify its current holder, and stop without changing repository or workflow state.

This file-based coordination is a convention among trusted tasks, not a security or transaction boundary.

## Finish

Completion means the authorized endpoint and its applicable checks/reviews are satisfied. For an authorized merge endpoint, verify the merge, associated-branch closeout, and saved checkout on updated local `main`, preserving unrelated work. A local-only endpoint does not require publication. Ask whether to retain or delete the ignored session folder. Archive tasks only when the user asks.
