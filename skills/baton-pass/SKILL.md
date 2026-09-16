---
name: baton-pass
description: Deliver an explicitly selected Baton Pass task from an approved plan, with a Sol manager, optional bounded workers, and independent final review.
---

# Baton Pass

Minimize total work to a correctly completed outcome. The manager owns delivery and may implement directly; delegation is optional. Use Ponytail for implementation and instruction design.

## Authority and records

Reuse the user's selected roles, models, project, checkout, plan, and delivery endpoint. Ask through native input only for missing material decisions or authority; resume the authorized next step in the same turn when an answer resolves a gate.

Keep one manager per repository, bound with its workers to that repository's verified saved project and checkout. A user-selected shared architect may advise several repository managers from a recorded workspace project; each manager retains its own write and delivery boundaries. Native children belong to their dispatching parent. Record task identities from successful tool results, never from guessed IDs. Persistent role tasks use the titles `Architect`, `Manager`, `Worker`, and `Reviewer`.

Reuse the existing issue or approved plan as the sole specification. It owns outcomes, rationale, non-goals, ownership, dependencies, safeguards, and observable acceptance. Assignments reference it and add only their bounded work, relevant paths, dependencies, checks, and return evidence. The loaded skill owns coordination; session records and consuming skills must not copy its protocol or add competing staffing and review gates. Explicit user choices and domain-specific acceptance requirements still apply.

Reuse existing session records. For persistent handoffs, use a locally ignored `docs/baton-pass/<session-id>/`: `status.md` indexes repository/project and registered roles; `baton-control.md` holds overall ownership, candidate and next action; numbered batons hold delegated assignment ownership and correction history. Keep each fact in one owner and link to it elsewhere. Create only records needed for the selected roles; do not copy the plan or add a lifecycle service. Preserve existing evidence and correction history when resuming an older session.

## Plan

The initiating task starts in the role implied by the request. Substantial architecture belongs to the selected architect; use an Astra app task when selected, never an Astra planning subagent. Routine work with a settled contract needs no additional architect or planning phase.

The architect resolves consequential unknowns in the authoritative plan before affected implementation. Verify fragile external interfaces and ownership assumptions against actual behavior where they determine correctness. Read-only bounded research may be delegated; its result returns to the architect.

Complete required scientific or architectural design review, using a fresh Sol reviewer by default or the explicitly selected alternative. Reuse still-valid review. Obtain approval for material design decisions and the implementation endpoint when not already granted, then hand the approved plan to the manager. The architect remains available for material design questions; routine reversible implementation choices stay with the manager.

## Deliver

Use Sol for the delivery manager unless the user selected otherwise. Inspect the exact repository, branch and dirty state; reuse the task branch and preserve unrelated work. The manager owns implementation, testing, integration, acceptance, review disposition, and authorized Git/GitHub actions.

Implement directly when dispatch and verification would cost more than the work, or when integration, transactional rollback, security, or coupled changes need continuous ownership. Otherwise use an optional Luna worker at max effort for a clear, bounded assignment with independently checkable results. Honor existing staffing choices; choose within authorized defaults without asking again for every assignment. Read [worker transports](references/worker-transports.md) only when delegating.

Inspect substantive changes and the required behavior before acceptance. Preserve meaningful tests and safeguards through replacements; verify mocks against the real interface at consequential boundaries. Completion claims, test counts, revision labels, and smaller diffs are not substitutes for evidence.

A worker returns an unresolved material decision to the manager. Answer from the approved contract when possible; route architectural gaps or changed ownership to the architect, and obtain user decisions for changed scope or authority. Pause only dependent work. Never disguise an unresolved design decision as a worker assignment.

For findings and correction loops, follow [shared review recovery](/home/tnnrpolley21/.codex/references/review-control.md). Reassess after a failed correction; pause at recurrence or before a third automatic round. The manager may take over an in-scope remainder once the previous writer has stopped, without new implementation permission. Preserve the same acceptance boundary and correction history across worker, model, transport, and manager changes; takeover does not waive a recovery stop.

## Review and finish

After integration and required checks, identify the exact candidate and use one fresh independent read-only Sol reviewer by default. It checks the approved requirements, plan fidelity, safety boundaries, and evidence, with no helpers or mutations. Use existing plan/result pointers plus the candidate, base, relevant diff and limitations; do not rewrite a review specification. A required domain review may satisfy this gate when it covers the same candidate and contract.

Fable is an explicitly selected alternative. Exactly one `astra_final_reviewer` at `xhigh` may replace the ordinary final reviewer only with explicit user approval for this task after implementation; no other Astra subagent is permitted. There is no automatic architect → Fable → Astra cascade. Consult the architect again only for a material design question or explicitly requested architectural review.

The manager classifies findings against existing requirements; optional hardening creates no new work. Correct required defects, renew affected checks and independent review, and retain still-valid evidence. Reuse the independent reviewer when available; a changed candidate needs a current verdict, not another automatic review cascade. A consumed Astra review is never repeated.

Finish at the authorized endpoint. Use Git and GitHub guidance for commits, publication, merge and exact associated-branch closeout; push/PR and merge authority remain separate. Verify the accepted candidate and hosted head before delivery; pushing to armed auto-merge also requires merge authority. Report pending external gates honestly. Retain session evidence unless removal is authorized; archive tasks only when requested.

## Handoffs and continuation

Transport is a hard return boundary. A native child returns only through its native terminal result to its direct parent, and every assignment must say so. It does not discover, read, navigate to, or message app tasks even when those tools are callable.

Only the current holder transfers an app-task baton. Write the full assignment, result, or question and registered next holder in the ignored session record, then send only the routing line below to that registered task ID; never search task listings for a substitute or paste report content into the message prompt.

```text
$baton-pass session=<id> baton=<control-or-number> from=<sender-role> to=<recipient-role> action=<action> read=<absolute-session-path>
```

A successful direct-message result naming that exact recipient is delivery acknowledgement. Do not read the recipient to prove receipt or roll back a successful transfer. The sender may continue separate owned work; otherwise report delivery and end the turn. The recipient returns completion or blockers to the registered parent/manager, which resumes the authorized next step.

For a definitively failed send, retain the sender as holder and report the failure. For an ambiguous result or wrong recipient, preserve the evidence, leave affected work paused, and obtain direction before resending or reassigning; do not create competing writers.

The parent may work independently and use the supported event wait for outstanding native results; one wait need not return every child. Track returned identities and await each required result before integration or acceptance. Do not poll task status/logs, send progress nudges, or create goals, automations, timers, or watchers to supervise delegated work. App tasks return by message or a new user turn.

When resuming a session, read its current holder, candidate and unresolved gate rather than reconstructing state from old narratives. Retain in-flight owners and accepted decisions; replace obsolete workflow mechanics on the next handoff without restarting the task or resetting corrections. File-based batons coordinate trusted tasks; they are not a security or transaction boundary.
