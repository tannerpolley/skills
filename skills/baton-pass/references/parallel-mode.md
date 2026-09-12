# Parallel mode

Use this mode only after the manager finds at least two plan-approved assignments with disjoint responsibility and intended paths, no dependency on each other's unfinished work, and independent acceptance checks. Otherwise use sequential mode.

## Decision and topology

1. Present the numbered assignments and use native input to ask the user for sequential or parallel execution. Recommend parallel only when isolation is explicit; wait for the choice.
2. Record one clean base commit and the manager's candidate branch before creating workers. Baton 1 uses the saved checkout and candidate branch. For each later app-task worker, create it in the recorded project with `environment: {type: "worktree", startingState: {type: "branch", branchName: "<recorded-candidate-branch>"}}`. Concurrent native subagents are eligible only when the live tool guarantees one wait returns the complete set; the manager creates an explicit worktree and task branch for each from that base. CSE-Pi uses a separate result and candidate directory outside the source workspace.
3. Treat these worker worktrees, branches, and CSE-Pi candidates as the only exception to the shared-checkout and shared-branch rule. Architects and the manager remain in the saved checkout; all app tasks remain in the same project.
4. Once the manager exists, keep `status.md` as its index. In each `baton-<number>.md`, record that assignment's boundary, expected paths, transport, exact returned worker identity, worktree or candidate directory, branch and base when applicable, holder, state, and correction-round count. App-task and native-subagent workers edit only their baton file among session-control files; the manager records CSE-Pi state. Include the baton number in every artifact and handoff.
5. Dispatch only assignments whose boundaries remain disjoint. If an app task returns the wrong project, or any transport lacks its required isolation or identity, do not send work.

## Returns and integration

Each baton moves independently. A clarification pauses only its assignment; another independent worker may continue. The manager may inspect a returned secondary baton in its exact worktree or retained CSE-Pi result while other workers run, but must not edit a worktree whose worker still holds its baton or mutate the saved checkout while baton 1 is held by its worker.

The manager remains the sole Git owner. For each completed app-task or native-subagent baton, verify its worktree, branch, status, diff, boundary, and checks. Commit accepted baton 1 work on the candidate branch. For each later baton, commit accepted work on its task branch; after baton 1 returns, cherry-pick that exact commit onto the candidate branch. For CSE-Pi, verify the retained result identity, hashes, scope, candidate diff, and checks before applying accepted changes to the candidate branch. Retain every worker worktree, branch, and CSE-Pi result until integration and combined review are complete.

Any overlapping change, cross-assignment dependency, or integration conflict invalidates parallel isolation. Stop integration, preserve every branch and worktree, and route the boundary question through the advisory architect or user; do not make workers edit each other's assignments. Run combined checks and all independent reviews only after every implementation baton is integrated into one candidate.
