# Candidate rules for step 3

Let B(x) be the escalation decision from `model_in.json`: its logit is greater
than zero. Each candidate retains B(x) and adds one condition that forces
escalation. Outside that condition, the decision stays B(x).

1. **Error threshold 0.70:** Escalate if B(x) is true, or if
   `tier_critical == 1` and `error_rate >= 0.70`.
2. **Error threshold 0.72:** Escalate if B(x) is true, or if
   `tier_critical == 1` and `error_rate >= 0.72`.
3. **Error threshold 0.73:** Escalate if B(x) is true, or if
   `tier_critical == 1` and `error_rate >= 0.73`.
4. **Latency lowers the error threshold:** Escalate if B(x) is true, or if
   `tier_critical == 1` and `error_rate + 0.05 * latency_spike >= 0.75`.

All four candidates match all 32 labels in `evidence.csv`. Rows 1–16 change
from no escalation to escalation. Rows 17–32 keep their existing decisions.
These are hypotheses; the examples do not establish an exact threshold.
Earlier labels describe earlier steps and may be overridden by this correction,
as specified in `TASK.md`.

## Query design

All eight query rows have a negative logit in `model_in.json`. Thus, an added
condition directly determines each candidate's predicted label. Rows 1–6 pair
three error rates with low and high latency. Rows 7–8 test exact thresholds.
All other inputs stay fixed.

| Query row | error_rate | latency_spike | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 |
|---|---|---|---|---|---|---|
| 1 | 0.710 | 0.1 | 1 | 0 | 0 | 0 |
| 2 | 0.710 | 0.9 | 1 | 0 | 0 | 1 |
| 3 | 0.725 | 0.1 | 1 | 1 | 0 | 0 |
| 4 | 0.725 | 0.9 | 1 | 1 | 0 | 1 |
| 5 | 0.740 | 0.1 | 1 | 1 | 1 | 0 |
| 6 | 0.740 | 0.9 | 1 | 1 | 1 | 1 |
| 7 | 0.700 | 0.1 | 1 | 0 | 0 | 0 |
| 8 | 0.720 | 0.1 | 1 | 1 | 0 | 0 |

No model weights were changed.
