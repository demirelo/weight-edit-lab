# Candidate rules for step 3

Let B(x) be the current model decision: 1 if its logit is greater than zero, otherwise 0.
Each candidate forces escalation when its condition holds. Otherwise, it preserves B(x), including the earlier corrections.

1. **Threshold 0.60:** Escalate if `tier_critical == 1` and `error_rate >= 0.60`; otherwise use B(x).
2. **Threshold 0.65:** Escalate if `tier_critical == 1` and `error_rate >= 0.65`; otherwise use B(x).
3. **Threshold 0.70:** Escalate if `tier_critical == 1` and `error_rate >= 0.70`; otherwise use B(x).

Each candidate matches all 32 labelled examples. Rows 1–16 change from 0 to 1. Rows 17–32 retain the current model decision. The examples leave the threshold uncertain: the negative critical-tier example at error rate 0.594 and the changed positive example at 0.700 do not distinguish these candidates. These thresholds are hypotheses, not an exhaustive set of possible rules.

## Query design

The eight inputs copy evidence row 16, counting data rows from 1. Only `error_rate` changes. The current model returns a negative logit for every query, so its existing decision cannot hide the override. The inputs test the candidate thresholds, values just below them, and two values between them.

| Query row | Error rate | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---:|---:|---:|---:|
| 1 | 0.5999 | 0 | 0 | 0 |
| 2 | 0.6000 | 1 | 0 | 0 |
| 3 | 0.6250 | 1 | 0 | 0 |
| 4 | 0.6499 | 1 | 0 | 0 |
| 5 | 0.6500 | 1 | 1 | 0 |
| 6 | 0.6750 | 1 | 1 | 0 |
| 7 | 0.6999 | 1 | 1 | 0 |
| 8 | 0.7000 | 1 | 1 | 1 |

Other answer patterns can reject all three candidates or narrow the threshold further. No model weights were changed.
