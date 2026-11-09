---
name: correct
description: Turn a mistake agents keep repeating in a repository into one that cannot happen, by structure first and instructions last. Use when the user says an agent made the same mistake again, asks to enforce a rule instead of restating it, or says "correct".
---

# Correct

The user keeps correcting agents in this repository for the same mistakes. Change the repository so the next agent cannot make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that passes. Design the repository so a change that looks right from one file is right for the whole repository.

## Find the mistake classes

Read recent commits, reverts, pull request review comments, the agent instruction files, and comments that explain workarounds. Inside T3 Code, thread history is evidence too (`t3_thread_search`). Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Types, then a check.** Make the bad state impossible to write. If bad code still passes, add a lint, hook or required check whose error names the file, type or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **A test of the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change.
4. **An instruction, last, and only for judgment calls.** Nothing fails when an agent skips it.

An architecture change is a material decision: present the class, its evidence and the smallest change, and wait for the user before making it.

## Fix and prove

Fix the most frequent classes first, one commit each. Prove each new check fails on a real past mistake, and run it the same way locally and in the repository's required checks. An exception goes on the offending line with a reason, an expiry date and the user's approval.

## Keep rule and enforcer together

In the repository's agent instruction file, name what enforces each rule beside the rule. When the user corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that is a repeat: fix it at the highest level in the same change. Remove a rule once its mistake cannot happen.

Reply with each class, its evidence, the level you picked, and why a higher level did not work.
