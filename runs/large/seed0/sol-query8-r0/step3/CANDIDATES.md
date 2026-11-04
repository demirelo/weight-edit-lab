# Candidate rules for step 3

Let B(x) be 1 when the model_in.json logit is greater than zero, and 0 otherwise.
Each candidate returns 1 when its condition is true. Otherwise, it returns B(x).
All comparisons below are strict.

1. **Error threshold 0.70:** Escalate when tier_critical = 1 and error_rate > 0.70.
2. **Error threshold 0.72:** Escalate when tier_critical = 1 and error_rate > 0.72.
3. **Error threshold 0.60:** Escalate when tier_critical = 1 and error_rate > 0.60.
4. **Combined error and latency:** Escalate when tier_critical = 1 and error_rate + 0.20 * latency_spike > 0.75.

Each candidate matches all 32 labelled examples. The first 16 examples change
from 0 to 1. The remaining 16 keep their original labels under each candidate.
These are hypotheses; the evidence does not establish one rule.

## Query design

All eight inputs have an original label of 0. Rows 1-6 test the error thresholds
and equality at 0.60, 0.70, and 0.72. Row 7 tests whether high latency can cause
escalation at a lower error rate. Row 8 checks a condition shared by all candidates.
Other feature values stay the same across rows.

Expected labels, in query.csv row order:

| Row | error_rate | latency_spike | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.60 | 0.01 | 0 | 0 | 0 | 0 |
| 2 | 0.65 | 0.01 | 0 | 0 | 1 | 0 |
| 3 | 0.70 | 0.01 | 0 | 0 | 1 | 0 |
| 4 | 0.71 | 0.01 | 1 | 0 | 1 | 0 |
| 5 | 0.72 | 0.01 | 1 | 0 | 1 | 0 |
| 6 | 0.73 | 0.01 | 1 | 1 | 1 | 0 |
| 7 | 0.65 | 0.90 | 0 | 0 | 1 | 1 |
| 8 | 0.75 | 0.01 | 1 | 1 | 1 | 1 |

Each candidate gives a different sequence of eight labels.
