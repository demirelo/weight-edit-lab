# Candidate rules

Let `f(x)` be the logit from `model_in.json`, `e = region_eu`, and `i = impact`. Escalate exactly when the proposed logit is greater than zero. These are hypotheses; the labels do not identify one unique rule.

| Candidate | Kind | Proposed rule |
|---|---|---|
| A | Output shift | Use `f(x) + 20*e`. EU alerts receive a constant bonus of 20. |
| B | Input re-interpretation | Use `f(T(x))`, where `T` replaces impact with `i + 0.20*e` and leaves every other feature unchanged. Do not clip the transformed impact; its internal range is [0, 1.20]. |
| C | Interaction | Use `f(x) + 40*e*i`. The impact bonus applies only to EU alerts and grows with impact. |
| D | Output shift | Use `f(x) + 30*e`. EU alerts receive a constant bonus of 30. |

All four rules match all 32 labels in `evidence.csv`, checked with forward passes. The current model disagrees with 15 labels; all 15 are EU alerts that must change from suppress to escalate. For a constant EU bonus, the observed labels permit approximately `17.761888 < bonus <= 38.897990`. Thus, both 20 and 30 remain possible.

The current model has zero first-layer weights for `tone_anger`. Each candidate preserves this independence and preserves the current logit for non-EU alerts. No weights were changed, trained, or fitted.

## Query predictions

Rows below correspond to data rows in `query.csv`. All other continuous inputs equal 0.50. Each row has `tier_critical=0`, `region_eu=1`, and `maintenance_window=0`. All submitted inputs satisfy the required bounds.

| Row | Impact | Urgency | A | B | C | D | Current logit |
|---|---|---|---|---|---|---|---|
| 1 | 0.95 | 0.01 | 0 | 0 | 1 | 0 | -33.783597 |
| 2 | 0.35 | 0.98 | 0 | 1 | 0 | 1 | -23.630638 |
| 3 | 0.66 | 0.49 | 0 | 0 | 0 | 1 | -28.233018 |
| 4 | 0.38 | 1.00 | 1 | 1 | 0 | 1 | -17.893216 |
| 5 | 0.79 | 0.36 | 0 | 1 | 1 | 1 | -23.439183 |
| 6 | 1.00 | 0.01 | 0 | 0 | 1 | 1 | -27.864491 |

Rows 1 and 2 separate the interaction and input-change rules from the constant bonuses. Row 3 separates the two constant bonus values. These first three rows give each candidate a unique prediction sequence. Rows 4–6 check those distinctions at other impact and urgency values, including impact at its upper bound. The smallest absolute candidate logit across these queries exceeds 1.76, so none depends on numerical behavior at zero.

The prediction columns are hypotheses, not correct labels. Use `answers.csv` to reject candidates; if no candidate matches all answers, revise the hypotheses before editing.
