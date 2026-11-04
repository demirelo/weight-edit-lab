# Candidate rules

Let `B(x)` be the current model's decision: `logit(model_in, x) > 0`.
Each candidate returns 0 when its suppression condition holds. Otherwise,
it returns `B(x)`. All comparisons below are strict.

1. **C1 — Users and urgency:** Suppress when `maintenance_window == 1`
   and (`users_affected < 0.50` or `urgency < 0.50`).
2. **C2 — Higher users and urgency thresholds:** Suppress when
   `maintenance_window == 1` and (`users_affected < 0.60` or `urgency < 0.80`).
3. **C3 — Users and region:** Suppress when `maintenance_window == 1`
   and (`users_affected < 0.50` or `region_eu == 1`).
4. **C4 — Users times urgency:** Suppress when `maintenance_window == 1`
   and `users_affected * urgency < 0.60`.

Forward passes confirm that each candidate matches all 32 supplied labels.
These are hypotheses, not confirmed rules. A users-only cutoff cannot explain
the changed decision at 0.697 and the retained escalation at 0.684.

# Query design

All eight queries retain the other features from evidence row 1. The current
model escalates all eight, so suppression changes their labels directly.
Rows 1–6 distinguish threshold, region, and product conditions. Rows 7–8
test either side of the proposed 0.50 users threshold at maximum urgency.
The labels below are predictions, not answers.

| Query row | Users | Urgency | EU | C1 | C2 | C3 | C4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.550 | 0.950 | 0 | 1 | 0 | 1 | 0 |
| 2 | 0.650 | 0.850 | 0 | 1 | 1 | 1 | 0 |
| 3 | 0.800 | 0.600 | 0 | 1 | 0 | 1 | 0 |
| 4 | 0.800 | 0.950 | 1 | 1 | 1 | 0 | 1 |
| 5 | 0.800 | 0.400 | 0 | 0 | 0 | 1 | 0 |
| 6 | 0.900 | 0.700 | 0 | 1 | 0 | 1 | 1 |
| 7 | 0.499 | 1.000 | 0 | 0 | 0 | 0 | 0 |
| 8 | 0.501 | 1.000 | 0 | 1 | 0 | 1 | 0 |

No model weights were changed or fitted.
