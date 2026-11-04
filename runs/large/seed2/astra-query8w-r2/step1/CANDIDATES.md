# Candidate rules

Let `f(x)` be the original model logit. Each rule escalates only when its resulting logit is greater than zero. These are hypotheses, not confirmed corrections. Forward passes confirm that each rule matches all 32 evidence labels. No weights were changed or fitted.

1. **A — Input re-interpretation: ignore anger.** Set `tone_anger` to zero, then evaluate the original model. Keep all other inputs unchanged. This is the leading hypothesis: it removes all 16 observed false escalations and preserves all 16 near-miss labels.

2. **B — Output shift: apply a context penalty.** Subtract 65 from `f(x)` when `confidence <= 0.2` or `maintenance_window == 1`. Otherwise, subtract 40. This tests whether a stricter escalation threshold explains the labels while the model still uses anger. The penalty values and conditions are provisional.

3. **C — Interaction: let error rate control anger.** Replace `tone_anger` with `min(tone_anger, max(0, 20 * (error_rate - 0.95)))`, then evaluate the original model. Keep all other inputs unchanged. Anger has no effect at error rates up to 0.95. Above that value, the permitted anger input rises to 1 at error rate 1. This tests whether strong error evidence permits anger to affect escalation. The threshold and slope are provisional.

# Query design

Rows 1 and 2 distinguish all three kinds. Row 3 tests the effect of removing anger from row 2. Row 4 tests whether a penalty suppresses an alert that escalates without anger. Rows 5 and 6 test the proposed interaction near its activation threshold. Rows 7 and 8 test the proposed confidence boundary.

Predictions below are candidate predictions, not supplied labels. Row numbers count data rows in `query.csv`.

| Row | A | B | C |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 1 | 1 |
| 3 | 0 | 0 | 0 |
| 4 | 1 | 0 | 1 |
| 5 | 0 | 1 | 0 |
| 6 | 0 | 1 | 1 |
| 7 | 0 | 0 | 0 |
| 8 | 0 | 1 | 0 |

The answers can reject these candidates. They cannot prove that a surviving rule holds everywhere.
