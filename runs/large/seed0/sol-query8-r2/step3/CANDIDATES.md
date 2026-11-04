# Candidate rules for step 3

Let `B(x) = 1` when the output logit from `model_in.json` is greater than zero.
Each candidate escalates when its condition is true. Otherwise, it returns
`B(x)`. Thus, each candidate keeps the earlier corrections unless this step
overrides them.

| Candidate | Condition that forces escalation |
| --- | --- |
| A: Error threshold 0.70 | `tier_critical == 1 AND error_rate > 0.70` |
| B: Error threshold 0.60 | `tier_critical == 1 AND error_rate > 0.60` |
| C: Error threshold 0.73 | `tier_critical == 1 AND error_rate > 0.73` |
| D: Error and latency threshold | `tier_critical == 1 AND error_rate + 0.10 * latency_spike > 0.75` |

All four candidates match all 32 labels in `evidence.csv`. Each changes the
same 16 baseline decisions from 0 to 1 and keeps the other 16 decisions.
Earlier evidence files contain labels from earlier steps; a step 3 condition
can override those labels.

The changed examples have `error_rate >= 0.73881524015888633`. The current
critical-tier examples labelled 0 have `error_rate <= 0.53213226407972691`.
This gap permits different thresholds. It also permits a latency-dependent
threshold. None of these rules is confirmed.

## Query design

All query rows have baseline decision 0. Only error rate and latency vary.
Rows 3 and 4 test the boundary at 0.70. Rows 5 and 6 test latency at a fixed
error rate. Rows 7 and 8 test the threshold at 0.73.

| Query row | Error rate | Latency | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.65 | 0 | 0 | 1 | 0 | 0 |
| 2 | 0.69 | 1 | 0 | 1 | 0 | 1 |
| 3 | 0.70 | 0 | 0 | 1 | 0 | 0 |
| 4 | 0.700001 | 0 | 1 | 1 | 0 | 0 |
| 5 | 0.72 | 0 | 1 | 1 | 0 | 0 |
| 6 | 0.72 | 1 | 1 | 1 | 0 | 1 |
| 7 | 0.73 | 0 | 1 | 1 | 0 | 0 |
| 8 | 0.74 | 0 | 1 | 1 | 1 | 0 |

These are candidate predictions, not supplied labels. Each candidate has a
distinct prediction sequence. No model weights were changed.
