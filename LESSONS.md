# Lessons (mistakes and their guards)

Read before launching runs here.

| Date | Mistake | Guard |
|---|---|---|
| 2026-11-03 | `lab.load` assumed 6 inputs; all 18 large chains crashed at once. | `harness.py smoke <task> <seed>` runs a no-op editor end to end. Run it for every task before any launch. |
| 2026-11-03 | `lab.save` wrote the small task's feature names for every task. | Same smoke test (it caught this one). |
| 2026-11-03 | Leak check matched the variable `evidence_passed`; `re.findall` with a group returned empty strings. | Tight regex `LEAK_RE`, `finditer`; smoke test asserts it hits real leaks and ignores look-alikes. |
| 2026-11-03 | Baseline repeated evidence 40x regardless of size, so 2,048 labels scored worse than 128. | Evidence share set by ratio, re-tuned per label count; `analyze.py` prints BASELINE WARNING if the curve drops by 2+ points (fires on the old curve). |
| 2026-11-03 | Token counts parsed wrong (`17'473` read as 17). | `analyze.py` re-parses tokens from logs with any digit separator. |
| 2026-11-03 | zsh `rm` on a glob with no match aborted a `&&` chain; the launch silently never ran. | Launch commands go on their own line, never after a glob `rm`; confirm a process started before moving on. |
| 2026-11-03 | Wrote a guessed time to the work board. | Take every board timestamp from `date -u +%FT%TZ`. |
| 2026-11-04 | Leak check flagged an editor's own helper `def target(x)`. | Dropped that pattern (file paths still catch real reads); smoke test asserts it is not flagged. |
| 2026-11-04 | Reported "0 of 40 contradicting labels" from a check run while one chain was still writing; true count 2 of 48. | Aggregate checks run only after `pgrep -f "harness.py edits"` shows nothing alive; state the count with its denominator. |
| 2026-11-04 | Unquoted URL with `?` failed in zsh (glob "no matches found"). | Always quote URLs in shell commands. |
| 2026-11-04 | Laya embedding on MPS hung silently mid-run; progress was hidden by a buffered pipe. | Laya runs on CPU; long jobs print progress with flush and are not piped through grep. |
| 2026-11-04 | Laya fine-tune baseline grid topped out at its edge (lr 1e-3, 1,000 steps) and I nearly reported it. | `laya_analyze.py` prints GRID EDGE WARNING when a best setting is at a grid edge; widen and rerun before reporting. |
| 2026-11-04 | First push rejected: commit used the real email while the GitHub account keeps email private. | Commit public repos with the account no-reply address (`<id>+<login>@users.noreply.github.com`). |
| 2026-11-04 | Compared Opus (CLI default effort) with Astra/Sol (high) without noting it. | Harness passes an explicit effort per editor and records it in done.json; tables carry an Effort column. |
| 2026-11-04 | "Target fixed" column covered only the last correction but read like all of them. | Report "All corrections fixed" (all corrected messages); define every column under its table. |
| 2026-11-04 | Hidden Laya test cache sat in laya/cache, reachable from the editors tool path (an editor noticed it and did not open it). | Move the test cache outside the lab after current runs; smoke test asserts no test data under paths given to editors. |
| 2026-11-04 | Laya step-2 edit (Fable): the option gate was centred on the midpoint, so every cards option got the full bonus and all evidence went to cards. | Editor check script prints the bonus on non-target messages (99th percentile and max) and on non-target options before any file is accepted; a 99th percentile above 0 fails the build. |
| 2026-11-04 | A waiter loop `until ! pgrep -f "<script>"` matched its own command line again (repeat of 2026-11-03), so it would never exit. | Waiters match the interpreter: `pgrep -f "Python.*<script>"`, and are tested once to return 0 with nothing running. Stronger guard than a note. |
