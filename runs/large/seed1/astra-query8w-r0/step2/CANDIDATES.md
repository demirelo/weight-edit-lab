# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Let `E` be
`region_eu`, `I` be `impact`, and `U` be `urgency`. Each candidate escalates
if its proposed logit is greater than zero. A zero logit suppresses the alert.

1. **A — Output shift.** Use `f(x) + 20*E`. EU alerts receive a constant
   bonus of 20. Other alerts keep their current logit.
2. **B — Input re-interpretation.** Apply the current model to an input with
   `impact = min(1, I + 0.16*E)`. Keep all other inputs unchanged.
   This raises the interpreted impact of EU alerts, subject to the input limit.
3. **C — Interaction.** Use `f(x) + E*(10 + 20*U)`. EU status changes the
   effect of urgency: the added bonus rises from 10 to 30 as urgency rises
   from zero to one. Other alerts keep their current logit.

These are hypotheses, not confirmed rules. Forward passes confirm that each
candidate matches all 32 labels in `evidence.csv`, including the 16 changed
labels and all 16 unchanged labels. Their minimum signed logit margins are
2.115856, 1.187387, and 4.808728, respectively.

The current model has zero first-layer weights for `tone_anger`. Each candidate
preserves this independence. No model weights were changed or fitted.

# Query design

Rows below refer to data rows in `query.csv`, starting at one. All unspecified
features in each query equal 0.5. Predictions are candidate predictions; the
correct labels are still unknown.

| Row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | Test the larger urgency-dependent bonus at maximum urgency. |
| 2 | 1 | 0 | 0 | Test a constant bonus when impact cannot increase and urgency is zero. |
| 3 | 1 | 1 | 0 | Test the smaller urgency-dependent bonus at low urgency. |
| 4 | 1 | 0 | 1 | Test input saturation against both output bonuses. |
| 5 | 0 | 1 | 0 | Separate the impact change from both output bonuses. |
| 6 | 0 | 1 | 1 | Separate the constant bonus from the other two rules. |
| 7 | 1 | 1 | 1 | Check a logit threshold just below a bonus of 20. |
| 8 | 0 | 1 | 0 | Check a logit threshold just above a bonus of 20. |

The first four rows separate the rule types with margins above four logit
units. Rows 5–8 examine smaller differences. Rows 7 and 8 differ only in
impact (0.73 versus 0.72); both have urgency 0.5. Their current logits are
-19.508106 and -20.806939. If a constant EU bonus is correct and these rows
receive labels 1 and 0, its value must be greater than 19.508106 and at most
20.806939, subject to the displayed rounding.

Queries were selected through forward passes on a fixed input grid. No training,
parameter fitting, or model edits were performed. The labels may reject all
three hypotheses; matching the supplied examples does not establish a rule.
