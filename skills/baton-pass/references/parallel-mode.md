# Parallel mode

Use this mode only after the manager finds at least two plan-approved assignments with disjoint responsibility and intended paths, no dependency on each other's unfinished work, and independent acceptance checks. Otherwise use sequential mode.

## Decision and topology

1. Present the numbered assignments and use native input to ask the user for sequential or parallel execution. Recommend parallel only when isolation is explicit; wait for the choice.
2. Record one clean base commit and the manager's candidate branch before creating workers. Create baton 1 in the same recorded project with `environment: {type: "local"}` so it uses the saved checkout and candidate branch. Create every later worker in that project with `environment: {type: "worktree", startingState: {type: "branch", branchName: "<recorded-candidate-branch>"}}`; each must have its own Codex worktree and task branch.
3. Treat these extra worker worktrees and branches as the only exception to the shared-checkout and shared-branch rule. Architects, the manager, and baton 1 remain in the saved checkout; all tasks remain in the same project.
4. Once the manager exists, keep `status.md` as its index. In each `baton-<number>.md`, record that assignment's boundary, expected paths, exact returned worker task ID, worktree, branch, base commit, holder, state, and correction-round count. Each worker edits only its baton file. Include the baton number in every artifact and handoff.
5. Dispatch only assignments whose boundaries remain disjoint. If creation returns the wrong project or lacks the required worktree or branch identity, do not send work.

## Returns and integration

Each baton moves independently. A clarification pauses only its assignment; another independent worker may continue. The manager may inspect a returned secondary baton in its exact worktree while other workers run, but must not edit a worktree whose worker still holds its baton or mutate the saved checkout while baton 1 is held by its worker.

The manager remains the sole Git owner. For each completed baton, verify its worktree, branch, status, diff, boundary, and checks. Commit accepted baton 1 work on the candidate branch. For each later baton, commit accepted work on its task branch; after baton 1 returns, cherry-pick that exact commit onto the candidate branch. Retain every worker worktree and branch until its commit is integrated and combined review is complete.

Any overlapping change, cross-assignment dependency, or integration conflict invalidates parallel isolation. Stop integration, preserve every branch and worktree, and route the boundary question through the advisory architect or user; do not make workers edit each other's assignments. Run combined checks and all independent reviews only after every implementation baton is integrated into one candidate.
