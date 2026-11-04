# Candidate rules for step 2

Let `f(x)` be the current logit from `model_in.json`. Let `r = region_eu`,
`u = urgency`, and `d = sensor_drift`. Each candidate escalates exactly when
its proposed logit is greater than zero. Each candidate leaves non-EU inputs
unchanged.

## 1. Output shift: EU bonus

Proposed logit: `f(x) + 20*r`.

EU alerts receive a constant bonus of 20. This matches all 32 current labels.
The changed cases require a bonus greater than 16.1724679600. The EU cases
labelled zero permit a bonus of at most 22.1373199813. Thus, the examples
support a range of bonuses; they do not identify 20 uniquely.

## 2. Input re-interpretation: increase EU urgency

For EU alerts, replace urgency with `min(1, u + 0.2)`, then apply the current
model. Keep every other feature unchanged. For non-EU alerts, apply `f(x)`.

This matches all 32 current labels. It changes the input before the hidden
layers, so its effect can depend on the other features and urgency saturation.

## 3. Interaction: sensor drift reduces the EU bonus

Proposed logit: `f(x) + r*(24 - 8*d)`.

EU alerts receive a bonus that decreases from 24 to 16 as sensor drift
increases from zero to one. Non-EU alerts receive no bonus. This matches all
32 current labels and makes the effect of sensor drift depend on region.

## Verification and earlier correction

Forward passes gave these results. Row numbers exclude the CSV header.

| Candidate | Current labels matched | Minimum logit for label 1 | Maximum logit for label 0 | Earlier labels overridden |
| --- | ---: | ---: | ---: | --- |
| EU bonus | 32/32 | 3.827532 | -2.137320 | Step 1 rows 6, 8 |
| EU urgency increase | 32/32 | 0.404675 | -9.384199 | None |
| Sensor drift interaction | 32/32 | 4.476294 | -1.710285 | Step 1 rows 6, 8, 9 |

TASK.md permits later corrections to override earlier example labels. The
listed overrides are predictions for step 2, not claims that those historical
labels were wrong.

The inferred earlier correction removes the influence of `tone_anger` on the
decision. All its first-layer weights are zero. Each candidate preserves this
independence everywhere, including on the earlier examples.

## Selected candidate

Select **candidate 1: add 20 to the logit for EU alerts**. All 16 changed cases
are EU alerts with logits between -16.172468 and -1.307288. A constant EU bonus
explains those changes with one parameter. Candidates 2 and 3 remain possible;
the evidence does not establish a unique rule or bonus.

No model weights were changed. No query file was created.
