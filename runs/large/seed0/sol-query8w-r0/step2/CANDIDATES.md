# Candidate rules

Let `f(x)` be the unchanged `model_in.json` logit, `e = region_eu`,
and `r = error_rate`. Escalate when the candidate logit is strictly positive.
These are hypotheses, not confirmed rules. Each matches all 32 labels in
`evidence.csv`. Each retains the current model outside EU alerts.

1. **A — Output shift.** Use `f(x) + 18*e`.
   EU alerts receive a constant bonus. The labels permit a constant EU bonus
   greater than approximately 16.150445 and no greater than 22.082856.
   The value 18 is one testable candidate in this interval.

2. **B — Input re-interpretation.** Use `f(x')`, where
   `impact' = impact + 0.15*e`; retain every other input.
   Do not clip the modified impact at 1. The submitted query inputs remain
   within the required bounds; this hypothesis allows the internal modified
   input to exceed 1.

3. **C — Interaction.** Use `f(x) + e*(18 + 4*r)`.
   EU status changes the effect of error rate: the EU bonus increases from
   18 to 22 as error rate increases from 0 to 1.

The model already ignores `tone_anger`: all its first-layer weights for that
input are zero. All three hypotheses retain this property.

## Query design

Rows 1–3 distinguish the rule types first. Rows 4–8 test nearby decision
thresholds at low and high error rates. All unspecified continuous features
are 0.5. Each row has `tier_critical=0`, `region_eu=1`, and
`maintenance_window=0`.

| Query row | impact | error_rate | A label | B label | C label |
|---|---:|---:|---:|---:|---:|
| 1 | 0.930 | 0.05 | 0 | 1 | 0 |
| 2 | 0.500 | 0.95 | 0 | 0 | 1 |
| 3 | 0.525 | 0.95 | 1 | 0 | 1 |
| 4 | 0.940 | 0.05 | 1 | 1 | 1 |
| 5 | 0.915 | 0.05 | 0 | 0 | 0 |
| 6 | 0.490 | 0.95 | 0 | 0 | 1 |
| 7 | 0.510 | 0.95 | 0 | 0 | 1 |
| 8 | 0.532 | 0.95 | 1 | 1 | 1 |

Labels that contradict all three candidates will require a revised hypothesis.
No model weights were changed.
