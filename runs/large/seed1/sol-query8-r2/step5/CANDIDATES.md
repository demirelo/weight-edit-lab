# Candidate rules for step 5

Let `F(x)` be 1 when `model_in.json` returns a logit greater than zero, and 0 otherwise. Each candidate sets the label to 0 when its suppression condition is true. Otherwise, it keeps `F(x)`.

| Candidate | Suppression condition |
| --- | --- |
| A | `maintenance_window == 1` AND (`users_affected < 0.50` OR `urgency <= 0.60`) |
| B | `maintenance_window == 1` AND (`users_affected < 0.60` OR `urgency <= 0.60`) |
| C | `maintenance_window == 1` AND (`users_affected < 0.50` OR `region_eu == 1`) |
| D | `maintenance_window == 1` AND (`users_affected < 0.50` OR `urgency <= 0.80`) |

All four candidates match all 32 labels in `evidence.csv`. These are hypotheses; the examples do not establish the exact thresholds or conditions. Earlier evidence files contain historical labels that later corrections can override.

A rule that suppresses only maintenance alerts with `users_affected < 0.50` does not match all current labels: data row 18 has `users_affected = 0.69746`, a positive input-model logit, and label 0. Each candidate includes a different possible explanation for this case. Data rows 24 and 31 show that some maintenance alerts must still escalate.

## Query design

All eight query rows have positive input-model logits. Thus, a suppression condition changes each query's label. Rows 1–4 test the user threshold; rows 5–7 test the urgency condition; row 8 tests the EU condition. Row numbers exclude the CSV header.

| Query row | A | B | C | D |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 1 | 1 |
| 3 | 1 | 0 | 1 | 1 |
| 4 | 1 | 1 | 1 | 1 |
| 5 | 0 | 0 | 1 | 0 |
| 6 | 1 | 1 | 1 | 0 |
| 7 | 1 | 1 | 1 | 0 |
| 8 | 1 | 1 | 0 | 1 |

Each candidate predicts a different sequence. Answers can also reject all four candidates. No model weights were changed.
