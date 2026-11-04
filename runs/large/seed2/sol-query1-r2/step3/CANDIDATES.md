# Candidate rules for step 3

Both candidates match all 32 labels in `evidence.csv`. They are hypotheses;
the examples do not determine a unique rule.

## Shared behavior

Let B be the first activation in the last hidden layer of `model_in.json`.
This is the existing network branch before the separate EU contribution.
Keep escalation when B > 0.

For noncritical alerts, keep the existing EU rule: escalate when
`region_eu = 1` and `impact + urgency > 0.95`.

For critical alerts, replace escalation from the EU branch alone with the
error-rate condition below. This replacement is a hypothesis supported by
row 28: its current logit is about 0.13966, its B is zero, and its label is 0.
A rule that only adds escalations cannot explain that label.

## Candidate A: threshold 0.70

Escalate if B > 0, the noncritical EU rule applies, or
`tier_critical = 1` and `error_rate > 0.70`.

## Candidate B: threshold 0.72

Escalate if B > 0, the noncritical EU rule applies, or
`tier_critical = 1` and `error_rate > 0.72`.

## Query

`query.csv` contains one critical alert with `error_rate = 0.71`.
Its B and current logit are both zero. The EU rule does not apply.
Candidate A predicts 1; Candidate B predicts 0.

The answer separates these candidates. It does not resolve all other possible
rules, the exact threshold, or behavior at equality.
