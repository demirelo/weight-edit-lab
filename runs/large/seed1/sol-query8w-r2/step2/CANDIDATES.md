# Candidate rules for step 2

Let `f(x)` be the logit from `model_in.json`. Escalate when the candidate logit is greater than zero. Let `e = region_eu`, `i = impact`, and `u = urgency`.

The model ignores `tone_anger`: all 64 weights from this input are zero. The paired examples in `evidence_step1.csv` support this earlier correction. Each candidate keeps this property.

1. **Output shift.** Use `f(x) + 20*e`. EU alerts get a constant bonus of 20. Other alerts keep their current logit. The current examples permit a range of constant EU bonuses, with approximate bounds `(17.94530, 27.29703]`; 20 is a candidate value.
2. **Input re-interpretation.** Replace impact with `min(1, i + 0.25*e)`, then evaluate the current model. EU alerts get an impact increase of 0.25, with a maximum impact of 1. All other inputs stay the same.
3. **Interaction.** Use `f(x) + 30*e*(i + u)`. The EU bonus increases with impact and urgency. Other alerts keep their current logit.

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv`. These are hypotheses, not confirmed rules. Step 2 can override earlier labels for EU alerts.

## Query design

All unspecified real inputs are 0.5. Every row has `tier_critical = 0` and `maintenance_window = 0`. Rows 1-7 have `region_eu = 1`; row 8 has `region_eu = 0`.

Rows 1-3 separate the rule types first. Rows 4-7 test bonus size and impact saturation. Row 8 repeats row 3 outside the EU condition to test that condition.

| Query row | Impact | Urgency | Current logit | Output shift | Input re-interpretation | Interaction |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0.25 | -7.911 | 1 | 0 | 1 |
| 2 | 0.25 | 1 | -32.641 | 0 | 0 | 1 |
| 3 | 0.5 | 0.75 | -25.489 | 0 | 1 | 1 |
| 4 | 0.75 | 0.44 | -22.497 | 0 | 1 | 1 |
| 5 | 0.75 | 0.46 | -20.661 | 0 | 1 | 1 |
| 6 | 0.75 | 0.48 | -18.786 | 1 | 1 | 1 |
| 7 | 1 | 0.1 | -21.904 | 0 | 0 | 1 |
| 8 | 0.5 | 0.75 | -24.131 | 0 | 0 | 0 |

The last three columns contain predicted labels. No model weights were changed.
