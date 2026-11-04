# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Each rule escalates only when its resulting logit is greater than zero. All three rules match all 32 labels in `evidence.csv`. These rules are hypotheses; no model edit has been made.

1. **A — Input re-interpretation: ignore anger.** Set `tone_anger` to zero, then evaluate `f`. Keep all other inputs unchanged. This is the simplest candidate and the leading hypothesis.
2. **B — Output shift: apply an anger-band penalty.** Use `f(x) - 50` when `0.6 <= tone_anger <= 0.7`; use `f(x) - 65` otherwise. This candidate leaves the input interpretation unchanged. Its region-dependent penalties also explain every supplied label, although they require more assumptions than A.
3. **C — Interaction: count anger only for critical alerts with high confidence.** Evaluate the original input when `tier_critical == 1` and `confidence >= 0.8`. Otherwise, set `tone_anger` to zero before evaluation. Thus, confidence and service tier control whether anger affects the decision.

## Query design

Rows 2 and 4 separate the three rule types: their predicted label pairs are A = `(0, 1)`, B = `(0, 0)`, and C = `(1, 1)`. The other rows test the proposed thresholds and conditions.

| Query row | Purpose | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Critical alert, confidence 0.79: below C's threshold | 0 | 0 | 0 |
| 2 | Same alert, confidence 0.81: above C's threshold | 0 | 0 | 1 |
| 3 | Same as row 2, but noncritical: test C's tier condition | 0 | 0 | 0 |
| 4 | Zero anger and positive original logit: test B's remaining penalty | 1 | 0 | 1 |
| 5 | Anger 0.599: below B's lower band boundary | 1 | 0 | 1 |
| 6 | Same as row 5, anger 0.601: inside B's band | 1 | 1 | 1 |
| 7 | Anger 0.699: inside B's upper band boundary | 1 | 1 | 1 |
| 8 | Same as row 7, anger 0.701: above B's band | 1 | 0 | 1 |

All features not identified in the table equal 0.5, except `region_eu = 0` and `maintenance_window = 0`. Rows 4–8 have `tier_critical = 1` and `confidence = 0.5`. Row 4 has `impact = 0.85`; rows 5–6 have `impact = 0.7`; rows 7–8 have `impact = 0.65`.
