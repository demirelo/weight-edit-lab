# Candidate rules for step 5

These are hypotheses. The labels do not identify one rule yet. No model weights have changed.

Let `f(x)` be the logit from `model_in.json`, `m = maintenance_window`, `u = users_affected`, and `e = region_eu`. Escalate when the candidate logit is greater than zero.

## Shared assumption

Each candidate uses `g(x) = f(x) + 0.2*e - 0.1` before the maintenance correction. This adds 0.1 in the EU and subtracts 0.1 elsewhere.

This assumption is necessary for these specific candidates to match every label. A maintenance correction alone leaves three disagreements: evidence rows 18 and 19 have positive current logits (0.034 and 0.005) but label 0; row 22 has a negative current logit (-0.069) but label 1. The shared adjustment resolves these disagreements. It is unconfirmed. Queries 7 and 8 test its effect on a new pair of inputs.

## A: Fixed maintenance penalty

**Kind: Output shift.** Use `g(x) - 60` when `m = 1` and `u < 0.5`. Use `g(x)` elsewhere. A sufficiently large original logit can still cause escalation within this region.

## B: Maintenance suppression region

**Kind: Region override.** Force label 0 when `m = 1` and `u < 0.5`. Use `g(x) > 0` elsewhere. All other raw features can take any valid value in this region.

## C: Maintenance and user interaction

**Kind: Interaction.** Use `g(x) - 500*m*max(0, 0.5-u)` everywhere. Maintenance reduces the logit in proportion to the shortfall of users affected below 0.5. The penalty reaches zero continuously at 0.5.

All three candidates match all 32 labels in `evidence.csv`. The constants are hand-chosen hypothesis values. They are not confirmed parameter estimates. The largest current logit among rows 1–16 is about 51.13, so the fixed penalty of 60 suppresses each of these rows. The interaction penalty also suppresses each of these rows.

## Query design and predicted labels

The row numbers below refer to data rows in `query.csv`, excluding its header.

| Row | Purpose | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Test a maintenance case with a logit large enough to exceed the fixed penalty. | 1 | 0 | 1 |
| 2 | Test a maintenance case where the fixed penalty exceeds the logit but the interaction penalty does not. | 0 | 0 | 1 |
| 3 | Test the interaction close to the user threshold, at `u = 0.4999`. | 0 | 0 | 1 |
| 4 | Test the exact threshold, at `u = 0.5`. | 1 | 1 | 1 |
| 5 | Test just above the threshold, at `u = 0.5001`. | 1 | 1 | 1 |
| 6 | Repeat row 1 with maintenance off to test the maintenance condition. | 1 | 1 | 1 |
| 7 | Test the shared adjustment outside maintenance with `e = 0`. | 0 | 0 | 0 |
| 8 | Repeat row 7 with `e = 1` to test the EU adjustment. | 1 | 1 | 1 |

Rows 1 and 2 distinguish all three candidates: A predicts `(1, 0)`, B predicts `(0, 0)`, and C predicts `(1, 1)`. The other rows test threshold values and shared assumptions. Returned labels can reject all three candidates.
