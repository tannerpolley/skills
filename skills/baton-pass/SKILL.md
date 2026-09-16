---
name: baton-pass
description: Coordinate an explicitly selected Baton Pass workflow through architect, manager, worker, and independent review, preserving its planning and staffing gates.
---

# Baton Pass

Run one cooperative delivery workflow in one repository and its recorded project. Cross-repository delivery requires a separate Baton Pass session and manager for each repository. Use native Codex task and subagent tools.

Before planning or review disposition, read [shared review recovery](/home/tnnrpolley21/.codex/references/review-control.md). Keep acceptance, finding dispositions, and correction history in the existing plan, role artifacts, and handoffs.

## Hard boundary

Bind the workflow to the initiating task's exact in-app `projectId`. The initiating task and every persistent architect, manager, reviewer, and app-task worker must belong to that same project; native subagents must be direct children of a project-bound participant. Never create or reuse a projectless task or a task from another project. If the initiating task has no project or any participant cannot be verified against the recorded project ID, stop before creating or messaging roles and ask the user to continue from the intended project.

Title every participating in-app task or thread with exactly one role word: `Architect`, `Manager`, `Worker`, or `Reviewer`. Use the applicable word as the complete title at creation, and rename an existing or initiating task before it performs role work. Multiple in-app tasks with the same role use the same title. Include no session IDs, numbers, models, actions, status, punctuation, or descriptive text. Native subagents keep their host-assigned names. Stop before dispatch if an in-app title cannot be set or verified.

Run only during active user turns and use event-return coordination. Default to one native subagent and yield completely until its terminal result. Use concurrent native children only when the live tool contract explicitly guarantees one wait returns the complete set; otherwise choose app-task workers for parallel assignments. An app-task sender treats a successful `send_message_to_thread` result naming the exact registered recipient as the sole delivery acknowledgement and stops. Never create or use automations, scheduled tasks, heartbeats, cron, timers, delayed wakeups, background watchers, goals, `wait_threads`, repeated native-agent waits, status reads, log reads, or progress prompts to monitor delegated work. Make no post-send `read_thread` call and do not roll back the holder after successful delivery. Later progress arrives through a return baton or a new user turn. If CI or another external condition is still pending, report it and wait for a new user message.

Independent review occurs only after the design is complete and after implementation is complete. Between design approval and the integrated candidate, use no Fable invocation or reviewer subagent; Manager inspection and Worker verification remain part of implementation, not independent review.

This loaded skill is the sole authority for workflow and handoff mechanics. Session files own task-specific scope, evidence, and current state only; never copy protocol rules into them. If stale session text conflicts with this skill, follow this skill and report the stale text to the manager.

## Start

1. Inspect the saved project and repository without changing them. Confirm that the task is substantial enough to benefit from architect, manager, worker, and independent-review roles.
2. Inventory callable app-task, native-subagent, native-reviewer, Fable, and task-title tools; unavailable optional choices do not block the workflow. Use native input unless already decided to select `Manager-first` or `Architect-first`, the architect staffing, optional read-only research delegation, and one design reviewer: a fresh Sol `reviewer` at `xhigh` by default or Fable when explicitly selected. Astra is never a design reviewer. For Architect-first, also settle the future manager model and effort. Record identities only from successful tool results; never infer them from prose.
3. Verify the initiating task's exact saved `projectId`, require a clean GitHub-backed saved local checkout, and rename the initiating task `Manager` or `Architect` to match the selected start. Create `docs/baton-pass/<session-id>/`, add `/docs/baton-pass/` only to the checkout's local `.git/info/exclude`, and write `brief.md`, compact `status.md`, and `baton-control.md`. Record only the session, repository, project ID, start mode, topology, exact role task IDs, architect duty owners, design reviewer, execution mode, and baton-file index.
4. For Manager-first, the initiating task is the sole manager. Create one fresh app task titled exactly `Architect` in the recorded project and local checkout with the approved model and effort; give it the brief, session path, duties, control baton, and exact return handoff. Record its returned ID, set it as holder, send once, and stop.
5. For Architect-first, the initiating task owns planning and advisory duties by default. Record it as architect and holder, then continue with [Architect](#architect). Create no manager until the reviewed design and staffing are user-approved.

If task creation or a direct message has an ambiguous result, stop and show the user the known facts. Never retry automatically or create a replacement task without the user's direction.

## Architect

The architect is repository-read-only except for the ignored session folder. Planning duty owns initial research and design; advisory duty owns later design questions and plan-fidelity review. One architect task owns both by default, or separate architect tasks may own one duty each as recorded in `status.md`.

For approved research or retrieval, the architect may dispatch one fresh read-only Luna subagent at its installed configured effort with the complete bounded question. Multiple children require a live wait-all guarantee; otherwise use one evidence-lead child to gather and synthesize the packet itself. After dispatch, the architect yields completely and does not monitor or narrate progress.

When assigned planning duty:

1. Read the brief, repository instructions, relevant code, tests, and issue or specification.
2. Write `plan.md` with authorized outcomes/phases, non-goals, implementation approach, observable acceptance, material ownership decisions, important risks, and verification. Identify any genuinely independent, non-overlapping worker assignments and their expected paths and dependencies; keep optional experiments and future phases distinct from authorized implementation.
3. Recommend a worker transport, model, and effort for each candidate assignment. Explain the plan's explicitness plus the difficulty, duration, isolation, and evidence needs behind each recommendation. Role names do not imply model families.
4. After `plan.md` is complete, run the selected design review once on a self-contained packet containing the brief, plan, acceptance, non-goals, risks, and proposed staffing. A Sol reviewer is a fresh read-only native subagent with no helpers; Fable uses the `fable-review` skill. Require `PASS` or one bounded findings list limited to design defects, unsupported assumptions, missing acceptance, and overengineering.
5. Reconcile or disposition the findings in `plan.md`, then ask the user to approve or revise the reviewed design and staffing. Unresolved material scope or architecture choices remain user decisions.
6. After approval, return `plan-ready` to the registered Manager-first task. In Architect-first, create one fresh app task titled exactly `Manager` in the same recorded project and local checkout with the approved model and effort, record its exact returned ID, then send `plan-ready`. Set the manager as holder and stop.

When assigned advisory duty, act only on a manager handoff. For `design-question`, research only as needed, resolve the stated gap in `plan.md`, and return the same implementation baton as `clarification-ready` to the manager. Obtain user approval before changing an accepted outcome, non-goal, architecture or ownership decision, or acceptance criterion. For plan-fidelity review on the control baton, compare the local candidate with `brief.md` and `plan.md`, including the root no-overengineering rule. Reject bandaid layers that retain the diagnosed broken implementation. Return `PASS` or one consolidated findings list tied to requirements and evidence, distinguishing blockers from optional advice, then stop.

## Manager

The manager is the only role that mutates Git or GitHub. Enforce the root no-overengineering rule in assignments and acceptance: the only accepted repair removes all broken code within the diagnosed boundary and replaces it with the simplest correct solution. Never dispatch or accept bandaid layers over problematic code; preserve required behavior, safeguards, and unrelated work. Before every corrective dispatch, read and increment that baton's correction-round count. If the dispatch would begin a third round, follow shared review recovery instead of sending it.

At that recovery boundary, when evidence shows worker capability rather than a plan or design gap is the blocker, the manager uses native input to recommend either one fresh worker on a stronger available model or transport, such as Sol or Astra in an app task, or manager completion of the bounded remainder. State the failed acceptance evidence, attempt history, preserved work, and reason for the recommendation; wait for confirmation before creating the replacement or implementing. Keep the same numbered baton, assignment, and correction count without overlapping holders or resetting attempts. User-confirmed manager completion authorizes that bounded exception to worker implementation ownership.

1. Read the approved plan, verify the checkout, reuse or create the task feature branch, and preserve the same outcome, non-goals, acceptance, and correction history in every worker assignment. Worker assignments contain implementation only; route research, planning, and design through the architect. If plan or staffing approval is still pending, obtain it before worker creation.
2. Read [worker transports](references/worker-transports.md). Present only callable transport, model, and effort combinations, recommend one for each assignment, and use native input to ask the user to choose. Ask for sequential or parallel execution in the same decision when the plan exposes independent, non-overlapping assignments; never infer either choice.
3. Create one `baton-<number>.md` per worker containing its assignment, selected transport, manager as holder, state, and correction-round count; add only its path to the `status.md` index. Dispatch through the selected transport, then record the exact returned worker identity and transfer the baton as specified in its reference. Stop or yield after the sequential handoff or complete parallel dispatch batch as required by that transport. Continue only as a numbered baton returns or the user starts a new turn.
4. If a worker returns `clarification-needed`, do no implementation against that baton. Answer only when the accepted plan already resolves it unambiguously; otherwise set the advisory architect as that baton's holder, send a `design-question` handoff with the exact gap and evidence, and stop work on that baton. After `clarification-ready` returns, verify that `plan.md` contains the answer and any material change has user approval, then return the numbered baton with a revised assignment. Other independent batons may continue.
5. When completed work returns, inspect the complete diff and evidence for that numbered baton, including Serena use or its concrete fallback reason for supported code work. Verify that repairs replace the defective implementation at its responsible boundary rather than mask its symptoms. Classify findings before making tiny obvious in-scope replacements or returning that baton to its worker under shared recovery. In parallel mode, integrate returned work only as specified in its reference.
6. After every implementation baton is integrated, run required local checks and commit a coherent combined candidate. Prepare local review evidence: brief, approved plan, baton assignments, candidate SHA, relevant diff, changed paths, checks, and limitations. A published PR is not a local-review prerequisite.
7. Accept the integrated candidate as Manager, then pass the control baton to the registered advisory architect for plan-fidelity review. The architect checks only the approved design, acceptance, and root no-overengineering rule and returns `PASS` or one consolidated findings list. No other independent review runs during implementation.
8. After architect `PASS`, use native input to select the final reviewer. Default to one fresh Sol `reviewer` at `xhigh`; use exactly one `astra_final_reviewer` at `xhigh` only with explicit approval given now for this completed candidate. Supply a self-contained fixed-candidate packet and require read-only work, no helpers, no Git/GitHub or app-task mutation, and `ACCEPT` or concise evidenced violations. Optional hardening and new requirements are nonblocking.
9. Adjudicate findings before bounded Worker corrections. Any substantive change requires renewed Manager acceptance and a fresh Sol final review; repeat architect fidelity only when the change could affect the approved design. An Astra review is consumed when spawned and is never repeated. Preserve correction history and use shared review recovery before a third correction round.
10. After Manager acceptance, applicable architect `PASS`, and final-review `ACCEPT`, verify publication authority. A local-only endpoint finishes locally; otherwise obtain missing publication authority natively. Immediately before push, verify HEAD, relevant index/worktree state, review evidence, remote target, and existing auto-merge state. A push that could trigger armed auto-merge also needs merge authority.
11. Push only the accepted candidate, create/update the authorized draft PR, and verify its hosted head. Hosted CI and required GitHub reviews that need publication remain merge gates afterward. Any branch update requires renewed affected evidence.
12. Present the exact PR, checks, reviewed head, and merge method. With existing or newly granted merge authority, revalidate the hosted head and request a guarded merge, or enable native auto-merge while hosted gates are pending. Honor existing merge-queue policy without introducing or bypassing one. A head guard is not a permanent lock on later pushes.
13. On observed merge, follow Git and GitHub for exact associated-branch closeout and return the saved checkout to updated local `main`. Pending auto-merge is not a completed merge.

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
