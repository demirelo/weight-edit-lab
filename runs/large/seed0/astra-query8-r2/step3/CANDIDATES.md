# Candidate rules

Let `B(x)` be the decision from `model_in.json`: escalate when its logit is greater than zero. Each candidate forces escalation when its condition holds. Otherwise, it keeps `B(x)`.

1. **A — Error threshold 0.60:** `tier_critical == 1` and `error_rate > 0.60`.
2. **B — Error threshold 0.70:** `tier_critical == 1` and `error_rate > 0.70`.
3. **C — Error threshold 0.73:** `tier_critical == 1` and `error_rate > 0.73`.
4. **D — Error and latency condition:** `tier_critical == 1` and `error_rate + 0.10 * latency_spike > 0.75`.

These are hypotheses, not confirmed rules. Forward checks show that each candidate matches all 32 labels in `evidence.csv`. Rows 1–16 change from no escalation to escalation. Rows 17–32 keep their current decisions.

For a rule with one error threshold, the critical-tier negative examples permit a threshold from 0.53213226407972691 up to, but not including, 0.73881524015888633. The examples do not establish whether latency changes that threshold.

The earlier evidence files contain labels from earlier steps. They establish historical behavior; a later correction can override those labels, as TASK.md states. These candidates keep the current model decision outside the proposed new condition.

# Query design

All eight query inputs have negative logits in the current model. Thus, an existing escalation cannot hide the effect of a candidate rule. All comparisons above are strict.

| Query row | Error rate | Latency spike | A | B | C | D |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.58 | 0.10 | 0 | 0 | 0 | 0 |
| 2 | 0.65 | 0.10 | 1 | 0 | 0 | 0 |
| 3 | 0.69 | 0.90 | 1 | 0 | 0 | 1 |
| 4 | 0.69 | 0.10 | 1 | 0 | 0 | 0 |
| 5 | 0.715 | 0.10 | 1 | 1 | 0 | 0 |
| 6 | 0.715 | 0.90 | 1 | 1 | 0 | 1 |
| 7 | 0.735 | 0.10 | 1 | 1 | 1 | 0 |
| 8 | 0.70 | 0.00 | 1 | 0 | 0 | 0 |

Rows 2, 5, and 7 separate the threshold candidates. Pairs 3–4 and 5–6 test the latency condition. Row 1 tests whether the threshold is lower than all three proposed thresholds. Row 8 tests the exact 0.70 boundary.
