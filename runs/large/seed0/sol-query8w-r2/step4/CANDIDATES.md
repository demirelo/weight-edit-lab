# Candidate rules for step 4

These are competing hypotheses, not confirmed rules. All three match all 32
labels in `evidence.csv` under forward evaluation. No weights were changed.
The evidence does not establish the proposed thresholds uniquely.

Let `f(x)` be the complete logit from `model_in.json`, including all earlier
corrections. Let `G` mean `confidence < 0.4` and `urgency > 0.2`.
Each candidate escalates exactly when its proposed logit is greater than zero.

## A. Output shift

Inside `G`, add a severity bonus:

`f_A(x) = f(x) + max(0, impact + urgency + error_rate - 1.01)`.

Outside `G`, use `f(x)`.

This hypothesis treats low confidence as a reason to add a bonus when the sum
of three severity features exceeds a threshold. It does not use a retry limit
or a users-affected limit.

## B. Region override

Force escalation inside this box of raw feature values:

- `confidence < 0.4`;
- `urgency > 0.2`;
- `users_affected < 0.88`;
- `retry_count < 0.98`.

Set the logit to `max(f(x), 1)` inside the box. Use `f(x)` elsewhere.
The users and retry bounds are speculative: they exclude the two difficult
near misses, rows 31 and 25 respectively, while retaining all changed rows.

## C. Input re-interpretation

Inside `G`, when `retry_count < 0.98`, form `T(x)` by replacing only `impact`
with `min(1, impact + 0.5)`. Use `max(f(x), f(T(x)))` there. Use `f(x)` elsewhere.

This hypothesis increases the impact used for evaluation while preserving any
existing escalation. Unlike B, it can still suppress an alert inside the box.
Unlike A, its result depends on the full model response to the modified input.

## Query design

Rows refer to one-based data rows, excluding CSV headers. Queries 1–4 separate
the rule types first. Queries 5–8 check proposed numerical thresholds.

| Query | Source and change | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Evidence row 25: retry_count = 0.5 | 0 | 1 | 1 |
| 2 | Evidence row 31: users_affected = 0.5 | 0 | 1 | 0 |
| 3 | Evidence row 5: users_affected = 0.95 | 1 | 0 | 1 |
| 4 | Evidence row 5: retry_count = 0.99 | 1 | 0 | 0 |
| 5 | Evidence row 3: severity sum = 1.009, by changing error_rate | 0 | 1 | 1 |
| 6 | Evidence row 3: severity sum = 1.011, by changing error_rate | 1 | 1 | 1 |
| 7 | Evidence row 5: confidence = 0.399 | 1 | 1 | 1 |
| 8 | Evidence row 5: confidence = 0.401 | 0 | 0 | 0 |

All table entries are candidate predictions, not received answers.

## Earlier evidence

All candidates preserve all 40 step 3 labels and every current escalation.
Earlier files contain labels from earlier stages; TASK.md permits later
corrections to override them. Relative to the current model, A and B predict
new escalations on step 1 rows 8, 10, 11, 12, 16, 19, 22; C predicts them on
rows 8, 11, 16. A and C predict new escalations on step 2 rows 22, 25, 32, 35,
36, 37; B also predicts one on row 24. These are proposed step 4 overrides,
not verified new labels. The input model already differs from step 1 labels
on rows 4, 6, 18.
