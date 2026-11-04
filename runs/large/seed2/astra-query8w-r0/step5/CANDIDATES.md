# Candidate rules for step 5

These are hypotheses, not confirmed corrections. No model weights were changed.

Let `f(x)` be the current logit from `model_in.json`. Let `m` be
`maintenance_window`, `u` be `users_affected`, and `r` be `region_eu`.
Define `G = (m = 1 and u < 0.50)`. Each candidate escalates only when its
specified logit is greater than zero. All other features retain their values.

## Evidence and a shared uncertainty

The first 16 examples have maintenance enabled and `u <= 0.420`; all require
suppression. This supports a maintenance rule, but does not establish its form
or threshold.

A maintenance box alone does not explain all labels. Evidence rows 18 and 19
have current logits 0.064 and 0.035 but labels 0. Row 22 has current logit
-0.039 but label 1. These rows lie outside G. Rows 18 and 19 have `r = 0`;
row 22 has `r = 1`.

All three candidates therefore include the secondary hypothesis
`b(x) = f(x) + 0.10 * (2*r - 1)`. This small regional shift reconciles those
three labels. The evidence does not prove that this is the intended cause.
Queries 6–8 test this shared assumption. A contrary answer can reject all
three candidates.

## A — Output shift

Use `b(x) - 60` inside G and `b(x)` outside G.

Maintenance adds a fixed penalty when few users are affected. A sufficiently
large current logit can still cause escalation. The penalty 60 exceeds the
largest current logit among the first 16 examples, approximately 56.6395.

## B — Region override

Use logit -1 inside G and `b(x)` outside G.

The raw-feature box `maintenance_window = 1, users_affected < 0.50` forces
suppression, regardless of alert strength. All other features are unrestricted.

## C — Interaction

Use `b(x) - 400 * m * max(0.50 - u, 0)`.

The maintenance penalty depends on the affected-user count. It decreases
linearly to zero as `u` approaches 0.50. Strong alerts can still escalate.
This differs from both a constant penalty and an unconditional override.

## Checks and query design

Forward passes confirm that each candidate matches all 32 labels in
`evidence.csv`. Constants were chosen by reasoning; no training or fitting
algorithm was used. This check does not establish preservation of all earlier
corrections or behavior on unseen inputs.

Query rows use the original feature order and contain no labels. The table
below gives candidate predictions, not correct labels.

| Query row | A | B | C |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 0 | 0 | 1 |
| 3 | 0 | 0 | 1 |
| 4 | 0 | 0 | 1 |
| 5 | 1 | 1 | 1 |
| 6 | 0 | 0 | 0 |
| 7 | 1 | 1 | 1 |
| 8 | 0 | 0 | 0 |

- Query 1 uses a strong alert with `u = 0.10`. It separates the fixed penalty
  from the override and interaction.
- Query 2 changes evidence row 3 to `u = 0.49`. It separates the interaction
  from the fixed penalty and override. Queries 1–2 give each candidate a
  distinct two-label signature.
- Queries 3–5 change evidence row 3 to `u = 0.449`, `0.451`, and `0.500`.
  They test whether suppression ends near 0.45 or 0.50, including the boundary.
- Query 6 disables maintenance in evidence row 18. It tests whether the
  unexplained suppression persists outside maintenance.
- Query 7 enables `region_eu` in evidence row 19. It tests the regional shift.
- Query 8 disables `region_eu` in evidence row 22. It tests the reverse change.

Evidence row numbers exclude the header. Correct query labels are pending.
