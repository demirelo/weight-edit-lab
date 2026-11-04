# Candidate rules

Let `B(x)` be the escalation decision from `model_in.json`: logit > 0.
Each candidate sets `escalate = 0` when its condition is true. Otherwise,
it preserves `B(x)`. All four candidates match all 32 labels in `evidence.csv`.
These are hypotheses. The evidence does not establish the exact thresholds
or whether the comparisons include equality.

| Candidate | Suppression condition |
| --- | --- |
| A: All maintenance alerts | `maintenance_window == 1` |
| B: Limited user impact | `maintenance_window == 1 AND users_affected < 0.50` |
| C: Wider user threshold | `maintenance_window == 1 AND users_affected < 0.60` |
| D: Limited user impact and service age | `maintenance_window == 1 AND users_affected < 0.50 AND service_age < 0.75` |

Candidate B is the leading hypothesis. The first 16 examples all have
`maintenance_window == 1` and `users_affected < 0.50`. However, the other
maintenance examples already have nonpositive input-model logits. Their labels
cannot exclude A or C. The first 16 examples also have `service_age < 0.75`,
so D remains possible.

## Query design

All eight query inputs have positive input-model logits, from 68.38 to 77.51.
Thus, a zero label indicates suppression under these candidates.
Rows 1-6 test the two user thresholds, including equality.
Rows 7-8 test the service-age condition on opposite sides of 0.75.
Other features remain fixed.

| Query row | users_affected | service_age | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.499 | 0.500 | 0 | 0 | 0 | 0 |
| 2 | 0.500 | 0.500 | 0 | 1 | 0 | 1 |
| 3 | 0.501 | 0.500 | 0 | 1 | 0 | 1 |
| 4 | 0.599 | 0.500 | 0 | 1 | 0 | 1 |
| 5 | 0.600 | 0.500 | 0 | 1 | 1 | 1 |
| 6 | 0.601 | 0.500 | 0 | 1 | 1 | 1 |
| 7 | 0.499 | 0.749 | 0 | 0 | 0 | 0 |
| 8 | 0.499 | 0.751 | 0 | 0 | 0 | 1 |

The columns give predicted labels, not confirmed answers. Answers that differ
from all columns require a revised hypothesis. No model weights were changed.
