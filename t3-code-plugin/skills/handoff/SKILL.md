---
name: handoff
description: Move this thread’s work into a fresh T3 thread when the owner asks to take over or start fresh; recommend it once after an observed context failure. Repository orchestrator transfers use the repository handoff workflow.
---

# Handoff

An explicit fresh-thread request authorizes a successor. An ordinary continue request stays here. An observed timeout or inaccessible context may justify one recommendation; compaction or turn counts alone do not. Wait for the owner's choice before creating work.

A repository root transfers ownership with `request_repository_handoff`. A managed issue worker returns a recovery handoff to its owner in its final result; it cannot replace its managed attempt with a top-level thread.

## Prepare

Reach a safe boundary and preserve pending approvals, active experiments and intentionally running processes. Read this thread's actual execution settings with `t3_thread_configure`; retain the exact model selection, options and modes rather than inferring defaults.

Fill [the handoff template](references/handoff-template.md) with observed facts. For scientific or diagnosis-heavy work, also use [the evidence checkpoint](references/evidence-first.md). Verify required artifact paths. Preserve authorized phases, non-goals, acceptance, review findings and correction history; a successor does not reset an unresolved recovery pause.

## Launch and verify

Launch with `t3_thread_launch`, the handoff as its message, and the observed source settings. Bind the successor to the actual checkout: continuing a worktree task requires the existing worktree strategy. Uncommitted work must remain in that same checkout. Keep the launch request ID for any identical retry.

Use `t3_thread_read` or `t3_thread_wait` to observe the successor. Creation alone is not verified continuation: require its known-good check and first authorized action, or its explicit preservation of a pending decision. A timeout, missing artifact, mismatched check or unavailable result leaves the source active. Retain the returned thread ID; uncertain setup is not a reason to launch a duplicate.

Only after concrete continuation is verified, archive the exact source with `t3_thread_organize`. Report the successor link and whether the source was archived or remains active awaiting verification.
