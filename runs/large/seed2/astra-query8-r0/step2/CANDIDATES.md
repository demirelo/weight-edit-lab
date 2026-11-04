# Candidate rules

Let I = impact, U = urgency, and B = the escalation decision from
`model_in.json`. Each candidate returns 1 when B is 1 or its condition below
is true. Otherwise, it returns 0. Thus, each candidate keeps all existing
escalations and adds an EU escalation condition.

1. **Sum above 0.95:** `region_eu = 1` and `I + U > 0.95`.
2. **Sum above 0.97:** `region_eu = 1` and `I + U > 0.97`.
3. **Weighted sum above 1:** `region_eu = 1` and `1.1*I + U > 1.00`.
4. **Sum with minimum values:** `region_eu = 1`, `I + U > 0.95`,
   `I > 0.20`, and `U > 0.20`.

All four candidates match all 32 labels in `evidence.csv`, as checked with
forward passes. The thresholds and extra conditions are hypotheses.
The evidence does not determine a unique rule.

# Query design

All eight query inputs have a negative existing logit. Therefore, an existing
escalation cannot hide a difference between candidates. Other features stay
fixed. Predictions below use exact decimal comparisons and strict inequalities.

| Query row | Impact | Urgency | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|---|---|---|---|---|---|---|
| 1 | 0.80 | 0.14 | 0 | 0 | 1 | 0 |
| 2 | 0.50 | 0.46 | 1 | 0 | 1 | 1 |
| 3 | 0.10 | 0.86 | 1 | 0 | 0 | 0 |
| 4 | 0.40 | 0.57 | 1 | 0 | 1 | 1 |
| 5 | 0.15 | 0.83 | 1 | 1 | 0 | 0 |
| 6 | 0.50 | 0.48 | 1 | 1 | 1 | 1 |
| 7 | 0.90 | 0.10 | 1 | 1 | 1 | 0 |
| 8 | 0.50 | 0.45 | 0 | 0 | 0 | 0 |

Rows 1–3, 5, and 7 separate the candidate rules. Rows 4 and 8 test exact
thresholds. Row 6 checks a shared positive prediction. The returned labels
can also reject all four candidates.

No model weights were changed. No training or fitting was used.
