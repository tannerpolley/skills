---
name: issues
description: GitHub issue work through T3 Code—queue or start an issue, delegate with an issue, propose issue changes, read the issue inbox, run a milestone, or change the repository orchestrator. Ordinary GitHub work uses github.
---

# Issues

Use T3's built-in issue instructions and the called tool's schema for operations and approvals. This skill covers recovery when issue work does not start.

## A queued issue that waits

In an ordinary thread, queuing is not a claim to implement the issue. If nothing starts, inspect `get_repository_orchestration`: distinguish a missing orchestrator from paused admissions, occupied slots, and an ineligible issue. With no registered root, use the repository controls to register one; repeatedly queuing the same issue cannot supply its owner.

## Refusals

- **Immediate-parent ownership:** a sibling worker cannot delegate another sibling's issue. Return the issue and refusal in your final result to its owner. The owner must dispatch at the correct level; changing the prompt or choosing a different model cannot repair ownership.
- **Explicit issue required:** check that the issue reference identifies the intended GitHub issue rather than merely mentioning its number in the task text.
- **Managed session cannot launch a thread:** for issue implementation, repair the issue delegation. A fresh top-level thread would lose the managed attempt's ownership and wake-up route.
- **Issue is ineligible:** inspect its native parent, blockers and state before retrying. A partial relationship read is not evidence that it has no blocker.

For `t3_issue_inbox`, list first and pass the returned event IDs to read; an issue number is not an inbox event ID.

## Changing the repository orchestrator

Choose the path by whether the current root is still active:

- **Active root, planned handoff:** use `request_repository_handoff` from that root. Retain it through approval and draining; launching a successor alone does not transfer ownership.
- **Stopped root, recovery:** read repository state, pause admissions, resolve remaining runs and unclaimed requests, then read state again before `restore_repository_root`. This keeps expectations current after cleanup. An unclaimed request can be cancelled with `cancel_issue_request`; a claimed attempt needs its own completion or cancellation. Restore leaves work paused, so check the restored owner before resuming.

A closed GitHub issue can still retain a suspended attempt. Treat `close_out_issue_attempt` as attempt cleanup rather than a substitute for changing the GitHub issue's state. If cleanup is refused, resolve the reported live work and re-read the revision before retrying.
