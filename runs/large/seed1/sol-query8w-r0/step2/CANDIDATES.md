# Candidate rules for step 2

Let `f(x)` be the unchanged logit from `model_in.json`. Each rule escalates only when its resulting logit is greater than zero. Let `E = region_eu` and `I = impact`.

All four rules match all 32 labels in `evidence.csv`, as checked by forward passes. These are hypotheses; the evidence does not identify one rule uniquely.

## A. EU bonus of 20

**Kind: Output shift.** Use `f(x) + 20*E`.

EU alerts receive a fixed bonus. Other alerts keep their current logit.

## B. Increase EU impact by 0.20

**Kind: Input re-interpretation.** Use `f(x')`, where `x'` equals `x` except that `impact' = min(1, I + 0.20*E)`.

EU alerts receive an impact increase, capped at 1. The model then computes its decision from the modified input.

## C. Make the EU bonus depend on impact

**Kind: Interaction.** Use `f(x) + 40*E*I`.

Impact has an additional effect when the alert is in the EU. The bonus is zero at impact 0 and reaches 40 at impact 1.

## D. EU bonus of 25

**Kind: Output shift.** Use `f(x) + 25*E`.

This alternative checks the unresolved bonus value. Both 20 and 25 match the evidence: the most negative changed logit is about -17.884, and the nearest EU negative example has a logit of about -27.265.

## Query design

Rows 1-3 separate the three kinds of rule. Row 4 separates the two fixed bonus values. Rows 5-8 check further combinations of predictions, including impact at its cap. All unspecified feature values are 0.5; every query has `region_eu = 1`.

The table gives candidate predictions, not correct labels. Row numbers refer to data rows in `query.csv`.

| Row | A | B | C | D |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 0 |
| 2 | 0 | 1 | 0 | 0 |
| 3 | 1 | 1 | 0 | 1 |
| 4 | 0 | 0 | 0 | 1 |
| 5 | 0 | 0 | 1 | 1 |
| 6 | 0 | 1 | 0 | 1 |
| 7 | 0 | 1 | 1 | 1 |
| 8 | 1 | 0 | 1 | 1 |

Here, 1 means escalate and 0 means suppress. No model weights were changed.
