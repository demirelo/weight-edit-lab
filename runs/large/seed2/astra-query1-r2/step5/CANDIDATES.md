# Candidate rules

These are hypotheses, not confirmed rules. Both reproduce all 32 labels in
`evidence.csv`. Row numbers below exclude the header. Earlier evidence files
describe earlier stages; their labels can be overridden by later corrections.

## Evidence and uncertainty

The first 16 examples have `maintenance_window = 1`, `users_affected < 0.42`,
and label 0. Examples 21 and 28 show that maintenance does not always prevent
escalation. The examples do not determine the exact users-affected cutoff.

A maintenance veto alone cannot match the supplied evidence. Example 18 has
`users_affected = 0.552284` and model logit about 0.014500, but label 0.
Example 22 has `maintenance_window = 0` and model logit 0, but label 1.
Thus, both hypotheses below include a second, provisional rule. The evidence
does not establish whether these mismatches reflect an earlier edit error or
another part of this correction.

## Shared provisional rule

Start with `escalate = (model_in logit > 0)`.

For alerts that meet all five conditions below, replace that decision with
`escalate = (region_eu == 1)`:

- `impact < 0.20`
- `tier_critical == 0`
- `confidence < 0.40`
- `users_affected > 0.50`
- `urgency > 0.60`

This condition selects examples 18, 19, and 22. It corrects examples 18 and 22
and preserves example 19. Its wider application is an assumption, not a result
proved by the examples.

## Candidate A: maintenance cutoff at 0.45

Apply the shared rule. Then force `escalate = 0` when
`maintenance_window == 1` and `users_affected < 0.45`.
Preserve the resulting decision everywhere else.

## Candidate B: maintenance cutoff at 0.50

Apply the shared rule. Then force `escalate = 0` when
`maintenance_window == 1` and `users_affected < 0.50`.
Preserve the resulting decision everywhere else.

## Query and validation

`query.csv` contains one alert with maintenance enabled and
`users_affected = 0.475`. Its current model logit is approximately 80.908071.
Its high impact excludes it from the shared provisional rule.

- Candidate A predicts label **1**.
- Candidate B predicts label **0**.

This query separates the two candidates. It does not validate the shared
provisional rule or determine the cutoff exactly. Both candidates passed a
forward-pass comparison against all 32 current labels. No weights were changed
and no model was trained or fitted.
