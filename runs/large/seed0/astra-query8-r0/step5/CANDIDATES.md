# Candidate rules

These are hypotheses for this step. Each matches all 32 labels in `evidence.csv`, as checked with forward passes. No model weights were changed.

Let `B(x)` mean `model_in.json` has a logit greater than zero. Each candidate returns 0 under its suppression condition below. Otherwise, it returns `B(x)`. All thresholds use strict `<`; equality does not trigger suppression.

| Candidate | Suppression condition |
|---|---|
| A | `impact < 0.20` OR (`maintenance_window = 1` AND `users_affected < 0.50`) |
| B | `impact < 0.20` OR `maintenance_window = 1` |
| C | (`impact < 0.20` AND `confidence < 0.20`) OR (`maintenance_window = 1` AND `users_affected < 0.50`) |
| D | `impact < 0.20` OR (`maintenance_window = 1` AND `users_affected < 0.60`) |

Maintenance-only rules cannot match every label. Evidence row 24 (counting data rows from 1) has `maintenance_window = 0`, `impact = 0.151`, and `confidence = 0.172`. Its model logit is approximately 0.020, but its label is 0. The low-impact clauses are possible explanations, not established rules. The evidence does not establish their thresholds or precedence over earlier corrections.

# Query design

All eight queries start from evidence row 31. Each has a positive input-model logit. Rows 1-5 change maintenance to 1 and vary users affected. Rows 6-8 keep maintenance at 0 and vary impact and confidence. Other features stay fixed.

Rows 2-5 distinguish maintenance scope and thresholds. Rows 6 and 8 distinguish unconditional low-impact suppression from suppression that also requires low confidence. Rows 1 and 7 check threshold boundaries. The answer vector can distinguish all four candidates. Other answer vectors can reject all four.

| Query row | A | B | C | D |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 1 | 0 |
| 3 | 1 | 0 | 1 | 0 |
| 4 | 1 | 0 | 1 | 1 |
| 5 | 1 | 0 | 1 | 1 |
| 6 | 0 | 0 | 1 | 0 |
| 7 | 1 | 1 | 1 | 1 |
| 8 | 0 | 0 | 1 | 0 |
