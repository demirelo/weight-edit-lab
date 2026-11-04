# Candidate rules for step 4

These are hypotheses. Each rule matches all 32 labels in `evidence.csv`.
The current model suppresses 15 examples that must escalate.

Let `f(x)` be the logit from the unchanged `model_in.json`.
Each candidate escalates if its resulting logit is greater than zero.
Use strict inequalities for all thresholds below.

Define these conditions:

- `L`: `confidence < 0.4`.
- `U`: `urgency > 0.6`.
- `I`: `impact > 0.65` and `users_affected > 0.4`.

## A: Add a logit bonus

Kind: **Output shift**.

Add 2.0 to `f(x)` when `L` and `U` hold.
Otherwise, add 1.5 when `L` and `I` hold.
Otherwise, use `f(x)`.
Apply only one bonus. A bonus can leave a sufficiently negative logit suppressed.

## B: Force escalation in two regions

Kind: **Region override**.

Set the logit to 1.0 inside either raw-feature box:

- `confidence < 0.4` and `urgency > 0.6`.
- `confidence < 0.4`, `impact > 0.65`, and `users_affected > 0.4`.

Leave all other features unrestricted in each box.
Use `f(x)` outside both boxes.

## C: Treat impact as maximal under low confidence

Kind: **Input re-interpretation**.

When `confidence < 0.4` and either `impact > 0.6` or `urgency > 0.6`,
replace `impact` with 1.0 before applying the current model.
Keep all other inputs unchanged. Use the original input outside this condition.
The current model can still suppress an alert after this input change.

## Query predictions

These are candidate predictions, not supplied correct labels.
The row numbers refer to `query.csv`.

| Row | A | B | C |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 0 | 0 | 1 |
| 4 | 1 | 1 | 0 |
| 5 | 0 | 0 | 0 |
| 6 | 0 | 0 | 1 |
| 7 | 1 | 1 | 1 |
| 8 | 0 | 0 | 0 |

Rows 1-3 distinguish all three kinds. Row 1 tests whether escalation is forced.
Row 2 tests a bonus that crosses zero while the input change stays suppressed.
Row 3 tests the input change outside the override boxes.

Rows 4-5 test the urgency threshold at 0.601 and 0.599.
Rows 6-7 test the impact threshold at 0.649 and 0.651.
Rows 7-8 test the confidence threshold at 0.399 and 0.401.

No model weights were changed.
