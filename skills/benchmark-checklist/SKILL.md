---
name: benchmark-checklist
description: Vet a timing, throughput or solver-cost number before reporting or acting on it. Use when you run a benchmark, or report a speedup, slowdown or regression you measured.
---

# Benchmark checklist

Use this when you produce a performance number: a before and after, a regression or no-slowdown claim, a solver wall time or iteration count, or a library or configuration choice. Answer each question with evidence from a run, not a guess about the code.

For a quick ballpark the user asked for, one run is enough. Still check questions 4 and 7, and say that it is one run. A choice between options is never a ballpark.

## Before you run

- Write down the claim you expect to make, in the words you would report ("the fit is 30% faster at the median on the 161-row dataset"), the result that would change a decision, and the noise floor. The questions test that sentence.
- Read the measurement script. Note what it times, counts, and ignores.
- Check the machine with `uptime`. Other agents share it, and a heavy job runs under `agent-heavy` with a 3-core quota (`AGENT_HEAVY_CORES`), so run both sides under the same quota. If the machine is busy and you cannot wait, interleave the sides so both see the same noise, and say so in the report.

## The questions

1. **Why not double?** Name the limiter. Profile in a run you do not report, because profilers slow the work down. Use CPU per process (`top`, `pidstat`), a runtime profiler (`perf`, `node --cpu-prof`, or one the project already installs), I/O wait, and syscall counts (`strace -c`), then map the hot spot to source. Under a core quota, the quota itself may be the limiter. If a change did not move the number, the limiter explains why, so find it before you call the change useless.
2. **Was it tuned?** Run every side the way real use runs it: release builds, the same flags and environment, the same thread and pool sizes, caches as warm or cold as real use sees them, and the same versions and data. If one side runs on defaults, you compared configurations, not implementations. A limiter that is a setting (a debug build, a missing index, a commit per row) means that side is untuned: tune it and measure again before you pick a winner.
3. **Did it break limits?** Do the arithmetic. Compare bytes per second with disk and network bandwidth, operations per second times cost per operation with your cores, and the time saved with the time the changed piece took. Removing a piece that takes 10% of the run can make the run at most about 11% faster. A result past a limit measured something other than the work, such as a cache, a no-op, or a bug.
4. **Did it error?** Count failures, non-converged cases and non-success responses, and check that outputs are correct, not just present. Rejections are often fast, and timeouts and retries are slow. If the script does not count errors, add the count.
5. **Does it reproduce?** Run each side at least 5 times, alternating (A, B, A, B, and so on) so warmup, caches, and drift favor neither. `hyperfine` does the repeats and statistics for a command. Report the median and range. A gap smaller than the run-to-run variation is no measurable difference.
6. **Does it matter?** Next to any micro result, measure the end-to-end path a user waits on, with realistic data sizes, and report the micro result as a share of the whole. A helper that takes 1% of a run can make the run at most 1% faster.
7. **Did it even happen?** Confirm the work ran inside the timed region: the cases were solved, the rows were written, the bytes were read, and the code used the result. Lazy code (generators nobody iterates, promises nobody awaits, results a compiler can discard) and timeouts produce numbers for work that never happened.

## Report

- Lead with the verdict: faster, slower, no measurable difference, or inconclusive.
- Give the number with its unit, the run count, the range, and the limiter. For example, "median 41 ms → 33 ms, 7 runs per side, range 32 to 35 ms after, bound by JSON parsing on one core."
- Call the verdict inconclusive when you claim a difference but cannot name the limiter, when a side ran untuned, or when you could not check questions 4 and 7. Name the gap.
- Keep the runs, range, and limiter evidence with the number, in the notes or a linked file.
