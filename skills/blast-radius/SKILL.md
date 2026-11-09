---
name: blast-radius
description: Find what a change could break outside its own diff, and prove the one fact that makes it safe by running real code. Use for "blast radius of X", "what could this break", or a small diff you do not trust yet.
---

# Blast radius

Find what a change breaks somewhere else, before it ships. Listing the callers is not the job: a search finds those in a second. The job is the breakage a search will not show you.

## Don't trust your own writeup

A blast-radius writeup that sounds right reads as convincing whether or not it is true. So do not hand back the writeup alone. Find the one or two facts the change's safety depends on and prove them by running code.

For each such fact, get it as far down this list as is cheap, and say where it stopped:

1. You said so. Worthless on its own.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You showed the bad case cannot happen, by walking the failure step by step.
4. You ran it: a script or test that calls the real code and fails loudly if you are wrong.
5. You reproduced it in the running application.

Step 4 is usually one small script that imports the same library the application ships and calls the exact function you are worried about.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes, and deletes, and what it now does differently, including the part the diff does not spell out. Read the commits and pull request for the stated intent.
2. **Find the one fact it is safe because of.** Most changes that look risky are safe because of a single fact, such as "this call only drops cache entries that are already dead". If it holds, most risky cases clear at once. Spend your time here, not on a long list of maybes.
3. **Look where a search stops.** Codebase Memory gives callers and impact inside one repository; go past it. Read the source of the library you call, at its pinned version, with any local patch. Work out when things run: startup, teardown, retries, concurrent actors. Follow what a symbol search misses: a serialized format, a database column, a wire format, another language or another repository reading the same bytes, a pinned package that downstream repositories install, a feature flag, code three hops downstream.
4. **Be honest about each risk.** Give it a real chance of happening and a real cost if it does. Keep the risks you confirmed and list the ones you checked and cleared separately. Cite a real `file:line`; a search that finds nothing is still an answer; never make up a caller or an interface.
5. **Prove the one fact.** Write a script or test that runs the real code, run it, and paste what happened.

## What to hand back

- **What it does.** What changed, including the part that is not obvious.
- **The one fact it is safe because of.** State it, say which step you got it to, and show the proof. If you could not prove it, write "unproven".
- **Risks.** Each names how it breaks, the `file:line`, how likely and how bad, and how to check. Paste the proof for the ones that matter.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test or reproduction that catches the real bug, including the script you wrote.
