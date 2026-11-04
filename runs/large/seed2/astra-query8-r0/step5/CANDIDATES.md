# Candidate rules for step 5

These are hypotheses, not confirmed rules. Each predicts all 32 labels in `evidence.csv` correctly. No weights were changed or fitted.

Let `B(x)` mean `model_in.json` returns a logit greater than zero. Each candidate applies its suppression rule first, then its promotion rule, then returns `B(x)`.

| Candidate | Suppress escalation when | Promote escalation when |
| --- | --- | --- |
| A | `maintenance_window = 1` and `users_affected < 0.45` | `maintenance_window = 0`, `region_eu = 1`, and `error_rate > 0.70` |
| B | `maintenance_window = 1` and `users_affected < 0.50` | Same as A |
| C | `maintenance_window = 1` and `users_affected < 0.525` | Same as A |
| D | `maintenance_window = 1` and `users_affected < 0.50` | `maintenance_window = 0`, `urgency > 0.60`, `users_affected > 0.50`, and `error_rate > 0.70` |

All conditions within a table cell must hold. Outside these conditions, keep the current model decision.

The evidence supports maintenance suppression but does not identify its exact threshold. The largest affected user fraction in the first 16 rows is 0.420. The smallest user fraction among positive maintenance examples is 0.532.

A suppression-only rule cannot match every supplied label: evidence row 22 (data rows start at 1) has label 1, but the current model returns exactly 0.0. Its maintenance flag is 0. The promotion clauses are provisional explanations of this discrepancy. The labels do not establish whether this is an earlier model defect or part of the new correction. These clauses must not be treated as confirmed changes.

## Query rows

Rows 1–5 copy evidence row 12 and change only `users_affected`. Their current model logits are positive. They test threshold intervals and equality conventions. Rows 6–8 copy evidence row 22 and change only urgency, EU region, or error rate. Their current model logits are zero. Rows 6–7 separate the two promotion hypotheses; row 8 tests their shared error-rate requirement.

| Query row | Changed feature | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | `users_affected = 0.450` | 1 | 0 | 0 | 0 |
| 2 | `users_affected = 0.475` | 1 | 0 | 0 | 0 |
| 3 | `users_affected = 0.500` | 1 | 1 | 0 | 1 |
| 4 | `users_affected = 0.515` | 1 | 1 | 0 | 1 |
| 5 | `users_affected = 0.525` | 1 | 1 | 1 | 1 |
| 6 | `urgency = 0.300` | 1 | 1 | 1 | 0 |
| 7 | `region_eu = 0` | 0 | 0 | 0 | 1 |
| 8 | `error_rate = 0.690` | 0 | 0 | 0 | 0 |

The values in this table are candidate predictions, not oracle answers. Other rules can also fit the evidence. Earlier evidence files describe earlier stages; this table checks the current 32 labels and does not claim to reconstruct every earlier correction.
