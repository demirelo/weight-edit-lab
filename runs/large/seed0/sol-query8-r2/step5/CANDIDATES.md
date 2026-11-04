# Candidate rules for step 5

Let `B(x)` be the escalation label from `model_in.json`: 1 when its logit is greater than zero, and 0 otherwise.

Each candidate sets the label to 0 when its condition applies. Otherwise, it retains `B(x)`. The suppression takes priority over earlier escalation rules. All four candidates match all 32 labels in `evidence.csv`, including the 10 labels that change from 1 to 0.

1. **Users below 0.5:** Suppress escalation when `maintenance_window == 1` and `users_affected < 0.5`.
2. **All maintenance alerts:** Suppress escalation whenever `maintenance_window == 1`.
3. **Users below 0.6:** Suppress escalation when `maintenance_window == 1` and `users_affected < 0.6`.
4. **Service age below 0.75:** Suppress escalation when `maintenance_window == 1` and `service_age < 0.75`.

Candidate 1 is the leading hypothesis. Every changed example has maintenance enabled and users below 0.5. However, the current evidence has no positive maintenance example to establish the limit. Every changed example also has service age below 0.75. The numerical limits above are hypotheses.

Earlier evidence records labels at earlier steps. A new suppression rule may override those labels where its condition applies. Outside that condition, each candidate retains the input model, including its earlier corrections.

## Query design

All eight query inputs have positive input-model logits. This lets each returned label test suppression directly.

Rows 1–3 test the 0.5 users boundary. Rows 4–5 test the 0.6 users boundary. Row 6 tests a higher users value. Row 7 tests a higher service age with low users. Row 8 disables maintenance as a control.

| Query row | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 |
| 4 | 1 | 0 | 0 | 0 |
| 5 | 1 | 0 | 1 | 0 |
| 6 | 1 | 0 | 1 | 0 |
| 7 | 0 | 0 | 0 | 1 |
| 8 | 1 | 1 | 1 | 1 |

The table contains candidate predictions, not supplied answers. Each candidate has a different prediction sequence. No model weights were changed.
