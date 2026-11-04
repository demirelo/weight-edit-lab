# Candidate rules

These hypotheses concern the new correction. Let `old(x)` be the escalation label from the unchanged `model_in.json`. Each candidate returns 1 when its condition holds; otherwise it returns `old(x)`.

Let `risk` mean `impact > 0.5 OR urgency > 0.6 OR error_rate > 0.8`.

- **A - Low confidence override:** Escalate when `confidence < 0.4 AND urgency > 0.2 AND risk`.
- **B - Wider confidence range:** Escalate when `confidence < 0.5 AND urgency > 0.2 AND risk`.
- **C - Combined risk score:** Escalate when `confidence < 0.4 AND urgency > 0.2 AND impact + urgency + error_rate > 1.01`.
- **D - Maintenance exception:** Apply A only when `maintenance_window = 0`.

All four candidates match all 32 labels in `evidence.csv`, including all 16 changed labels. They are hypotheses, not confirmed rules. The score threshold in C lies between the relevant negative example's score (1.003, row 31) and the smallest changed example's score (1.020, row 3).

## Queries

Rows refer to data rows in `query.csv`. All eight rows have an existing model label of 0. Each query retains the other features from evidence row 13.

| Row | Purpose | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | Test confidence 0.45 | 0 | 1 | 0 | 0 |
| 2 | Test high urgency with a low combined score | 1 | 1 | 0 | 1 |
| 3 | Test a high combined score below each separate risk threshold | 0 | 0 | 1 | 0 |
| 4 | Test maintenance scope | 1 | 1 | 1 | 0 |
| 5 | Test confidence exactly 0.4 | 0 | 1 | 0 | 0 |
| 6 | Test error rate exactly 0.8 | 0 | 0 | 1 | 0 |
| 7 | Test urgency exactly 0.2 | 0 | 0 | 0 | 0 |
| 8 | Test urgency just above 0.2 | 1 | 1 | 0 | 1 |

Rows 7 and 8 test the urgency boundary as a pair. The labels can reject every candidate; they do not have to select one. No model weights were changed.
