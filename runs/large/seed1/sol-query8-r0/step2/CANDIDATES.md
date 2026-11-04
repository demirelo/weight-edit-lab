# Candidate rules

Let `z` be the unchanged logit from `model_in.json`, `E` be
`region_eu`, and `M` be `maintenance_window`. Each rule escalates if its
adjusted logit is strictly greater than zero.

- **A: EU adjustment of 18.** Use `z + 18*E`.
- **B: EU adjustment of 20.** Use `z + 20*E`.
- **C: EU adjustment of 25.** Use `z + 25*E`.
- **D: EU adjustment depends on maintenance.** Use `z + E*(20 + 5*M)`.
  EU alerts receive 20 outside maintenance and 25 during maintenance.

All four rules match every label in `evidence.csv` (32 rows) and
`evidence_step1.csv` (37 rows). They preserve the model's independence
from `tone_anger`, whose input weights are zero.

The changed examples all have `region_eu=1`. Their original logits range
from approximately -17.884 to -1.165. The closest negative EU example in
the current evidence has a logit of approximately -27.265. This gap leaves
the adjustment amount and its dependence on maintenance unresolved.

## Query predictions

Rows follow the order in `query.csv`. Labels in this table are candidate
predictions; the correct labels must come from the next phase.

| Row | Maintenance | Original logit | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | -19.004 | 0 | 1 | 1 | 1 |
| 2 | 0 | -21.003 | 0 | 0 | 1 | 0 |
| 3 | 0 | -22.998 | 0 | 0 | 1 | 0 |
| 4 | 0 | -24.464 | 0 | 0 | 1 | 0 |
| 5 | 1 | -19.000 | 0 | 1 | 1 | 1 |
| 6 | 1 | -20.993 | 0 | 0 | 1 | 1 |
| 7 | 1 | -22.993 | 0 | 0 | 1 | 1 |
| 8 | 1 | -24.496 | 0 | 0 | 1 | 1 |

Each candidate predicts a distinct eight-label sequence. The inputs also
test several score levels within the unresolved interval. These candidates
are hypotheses; other rules can fit the available labels.

The model was read only. No model weights were changed or trained.
