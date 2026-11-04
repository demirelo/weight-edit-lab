# Candidate rules for step 4

Let `f(x)` be the supplied model's output logit. Escalate when the candidate
logit is greater than zero. Feature names below refer to the original input.
Each rule leaves inputs outside its stated condition unchanged.

## A. Region override

Force escalation inside this box:

- `confidence < 0.5`
- `urgency > 0.2`
- `retry_count < 0.98`
- `users_affected < 0.88`

Set the output logit to 1 inside the box; use `f(x)` elsewhere.
This rule treats low confidence and sufficient urgency as grounds for escalation,
with exceptions for high retry counts or many affected users. The evidence gives
weak support for those exceptions.

## B. Input re-interpretation

When `confidence < 0.5`, `urgency > 0.2`, and
`impact + urgency > 0.8`, replace impact with `min(1, impact + 0.5)`.
Apply the unchanged model to that modified input. Use `f(x)` elsewhere.

This rule increases effective impact for sufficiently urgent alerts with low
confidence. The model still controls the decision within the condition.

## C. Interaction — selected candidate

When `confidence < 0.5` and `impact + urgency > 0.8`, double urgency
before applying the unchanged model. Leave all other features unchanged.
Use `f(x)` elsewhere.

This rule makes urgency's effect depend on confidence and combined impact and
urgency. Do not cap the internal urgency value at 1: this candidate deliberately
reinterprets the input scale. External inputs retain their stated bounds.

## D. Output shift

Add this nonnegative bonus to the current output logit:

```text
bonus = max(0, min(
    0.5 - confidence,
    urgency - 0.2,
    impact + urgency - 0.8,
    max(error_rate - 0.1, impact - 0.7)
))
candidate_logit = f(x) + bonus
```

This rule gives a positive bonus when low confidence and sufficient urgency
coincide with sufficient combined impact and urgency, plus either an elevated
error rate or high impact. Unlike A, the bonus varies with the input.

## Evidence and selection

Forward passes confirm **32/32 matching labels in `evidence.csv` for every
candidate**. The supplied model matches 16/32. Rows 1–16 change from suppression
to escalation; rows 17–32 retain their labels under all four candidates.

Select **C** as the working hypothesis. Doubling urgency for all inputs with
`confidence < 0.5` already matches 31/32 labels. The combined-impact condition
excludes the remaining false positive, row 25. This gives C a simpler explanation
than A's retry/user exceptions or D's additional error-rate condition. B also
fits, but requires an extra urgency threshold and an impact cap.

This selection is tentative. The examples do not establish the exact thresholds,
the scale factor, or behavior outside their coverage. All current examples have
`maintenance_window = 0`; none tests the maintenance case. These candidates
define different rules beyond the observed examples.

The earlier files require separate interpretation: the supplied model disagrees
with step 1 rows 9, 11, and 16, and step 2 rows 22, 25, and 32. It matches all
step 3 labels. Thus, current-example agreement does not prove preservation of
all earlier corrections. No model edit or global preservation claim is made.

No training, fitting solver, or weight update was used. No query file was written.
