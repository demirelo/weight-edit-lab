# Candidate rules for step 4

These hypotheses each match all 32 labelled examples. The evidence does not establish one unique rule.

Let `f(x)` be the current model logit. Escalate when the candidate logit exceeds zero.
Let `R` be the following union of raw feature boxes:

```
confidence < 0.40 AND (
    impact > 0.85
    OR urgency > 0.65
    OR (impact > 0.65 AND urgency > 0.30)
    OR (users_affected > 0.70 AND urgency > 0.50)
)
```

All unlisted feature values are unrestricted. All comparisons have the strictness shown.

## A. Output shift

Add a fixed bonus of `1.60` to `f(x)` inside `R`. Elsewhere, use `f(x)`.
This rule can still suppress an alert inside `R` when its current logit is sufficiently negative.

## B. Region override

Force escalation inside `R`. Elsewhere, use the current model decision.
The four boxes express alternative conditions for sufficient alert severity at low confidence.

## C. Input re-interpretation

When `confidence < 0.40` and (`error_rate < 0.90` or `urgency > 0.50`), increase `impact` by `0.50`.
Apply the current model to that modified input. Elsewhere, apply the current model to the original input.
Keep every other feature unchanged. Do not clip the modified impact; it can exceed one.
This hypothesis changes the model input, so its effect depends on the other features.

## Query predictions

The rows follow the order in `query.csv`. Values are predicted escalation labels.

| Query | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | Separate a finite output bonus from an override. |
| 2 | 0 | 0 | 1 | Separate the input change from both region rules. |
| 3 | 1 | 1 | 1 | Test just below the input rule's error threshold. |
| 4 | 1 | 1 | 0 | Test at the input rule's error threshold. |
| 5 | 0 | 0 | 1 | Test at the region rules' urgency threshold. |
| 6 | 1 | 1 | 1 | Test just above that urgency threshold. |
| 7 | 1 | 1 | 1 | Test just below the shared confidence threshold. |
| 8 | 0 | 0 | 0 | Test just above that confidence threshold. |

Queries 1 and 2 separate all three kinds before the remaining queries test threshold values.
No model weights were changed.
