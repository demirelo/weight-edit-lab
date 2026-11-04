# Candidate rules for step 4

These are provisional hypotheses. Each rule matches all 32 labels in
`evidence.csv`. The examples do not establish a unique rule or exact thresholds.

For both candidates, let `I = impact`, `U = urgency`, `A = users_affected`,
and `C = confidence`. Apply the following decision when `C < 0.5`.
Keep the `model_in.json` decision when `C >= 0.5`.
The proposed decision replaces the full model decision in its stated scope,
including decisions from earlier corrections.

## Candidate 1: Combined severity

Escalate if and only if `C < 0.4` and either:

- `U > 0.65`; or
- `max(I, A) > 0.7` and `U + max(I, A) > 1.0`.

This rule permits high impact or a high affected-user count to compensate for
lower urgency.

## Candidate 2: Separate urgency requirements

Escalate if and only if `C < 0.4` and at least one condition is true:

- `U > 0.65`;
- `I > 0.85`;
- `I > 0.7` and `U > 0.3`;
- `A > 0.65` and `U > 0.5`.

This rule uses a separate impact threshold and fixed urgency requirements
for its remaining severity conditions.

## Query

The query has `I = 0.8`, `U = 0.25`, `A = 0.2`, and `C = 0.2`.
Candidate 1 predicts **1**, because `0.8 + 0.25 > 1.0`.
Candidate 2 predicts **0**, because all four conditions fail.
One binary answer separates these two candidates. It cannot establish that
either candidate is the intended rule outside the observed examples.
