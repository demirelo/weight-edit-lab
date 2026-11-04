# Step 4 candidate rules

Let `f(x)` be the unchanged `model_in.json` logit. Escalate when the proposed logit is greater than zero.

Define region `R` as:

`confidence < 0.4 AND urgency > 0.2 AND (impact > 0.45 OR urgency > 0.6)`.

This region is the union of two raw-feature boxes. All unspecified features span their full allowed ranges.

1. **A — Output shift.** Use `f(x) + 1.6` inside `R`. Use `f(x)` elsewhere. This gives qualifying alerts a fixed bonus, but can leave a sufficiently negative logit suppressed.
2. **B — Region override.** Force escalation inside `R` by using `max(f(x), 1)`. Use `f(x)` elsewhere. Unlike A, this always escalates a qualifying alert.
3. **C — Input re-interpretation.** If `confidence < 0.4`, replace `impact` with `min(1, impact + urgency * (1 - confidence))`. Keep all other inputs unchanged and evaluate the current model on those inputs. Otherwise use `f(x)`. Urgency increases interpreted impact more when confidence is low.

These are hypotheses, not established rules. Direct forward passes confirm that each matches all 32 labels in `evidence.csv`, including all 16 changed labels. The evidence does not establish the exact thresholds, bonus, or transformation. Historical labels belong to their original steps and can be superseded, as TASK.md states; the current model is the baseline for these proposed changes.

## Query predictions

Rows refer to data rows in `query.csv`. Predictions are candidate outputs, not supplied answers.

| Row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | Separate forced escalation from a finite bonus. |
| 2 | 1 | 1 | 0 | Separate output changes from input re-interpretation. |
| 3 | 0 | 0 | 1 | Test input re-interpretation outside the proposed boxes. |
| 4 | 0 | 0 | 1 | Test confidence just below 0.4 outside the boxes. |
| 5 | 0 | 0 | 0 | Test confidence just above 0.4 with the same other inputs. |
| 6 | 0 | 1 | 0 | Test a baseline logit just below -1.6. |
| 7 | 1 | 1 | 0 | Test a baseline logit just above -1.6. |
| 8 | 0 | 0 | 1 | Repeat row 3 during maintenance. |

The first three rows give each candidate a distinct answer pattern. Rows 4–7 test values after separating rule kinds. Row 8 tests an unobserved binary condition: every current evidence row has `maintenance_window = 0`.

No model weights were changed or fitted.
