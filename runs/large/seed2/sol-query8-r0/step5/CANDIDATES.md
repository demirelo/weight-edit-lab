# Candidate rules for step 5

All four candidates reproduce all 32 evidence labels, checked with forward passes. These are hypotheses. The evidence does not establish a unique rule.

Let `old` mean that `model_in.json` returns a logit greater than zero. Each candidate first sets the decision to `old OR promotion`, then sets it to 0 if its maintenance veto applies. The veto has priority.

The error promotion applies when all four conditions hold:
- `confidence < 0.40`
- `users_affected > 0.50`
- `urgency > 0.50`
- `error_rate > 0.70`

The EU promotion uses the first three conditions and `region_eu = 1` in place of the error condition.

| Candidate | Promotion | Maintenance veto: `maintenance_window = 1` and either condition holds |
| --- | --- | --- |
| A | Error promotion | `users_affected < 0.50` OR `urgency < 0.75` |
| B | Error promotion | `users_affected < 0.45` OR `urgency < 0.75` |
| C | Error promotion | `users_affected < 0.50` OR `urgency < 0.90` |
| D | EU promotion | `users_affected < 0.50` OR `urgency < 0.75` |

The first 16 examples support suppression during maintenance when few users are affected. Two other examples require attention: evidence row 18 has an old logit of 0.014 but label 0; row 22 has an old logit of 0 but label 1. A maintenance veto based only on `users_affected < 0.50` cannot explain both. The additional urgency and promotion conditions above are tentative explanations, not confirmed earlier corrections.

## Queries

Rows 1-4 use evidence row 21 as their reference. Rows 5-8 use evidence row 22. Row numbers exclude the header.

| Query row | Change from reference | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | users_affected = 0.47 | 0 | 1 | 0 | 0 |
| 2 | users_affected = 0.50 | 1 | 1 | 1 | 1 |
| 3 | users_affected = 0.55; urgency = 0.80 | 1 | 1 | 0 | 1 |
| 4 | users_affected = 0.55; urgency = 0.75 | 1 | 1 | 0 | 1 |
| 5 | region_eu = 0 | 1 | 1 | 1 | 0 |
| 6 | error_rate = 0.50 | 0 | 0 | 0 | 1 |
| 7 | error_rate = 0.70 | 0 | 0 | 0 | 1 |
| 8 | confidence = 0.40 | 0 | 0 | 0 | 0 |

Rows 1 and 3 separate the maintenance hypotheses. Rows 5 and 6 separate the promotion hypotheses. Rows 2, 4, 7, and 8 test proposed boundaries. Answers can reject all four candidates. No weights were changed, and no model output file was written.
