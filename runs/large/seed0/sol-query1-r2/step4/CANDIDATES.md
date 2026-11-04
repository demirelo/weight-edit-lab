# Candidate rules

Let `base(x)` mean that `model_in.json` produces a logit greater than zero.
Each candidate returns `base(x) OR trigger(x)`. Outside its trigger, it keeps
the current model decision. These are hypotheses, not confirmed rules.

## Candidate A: Combined severity

Trigger escalation when all conditions are true:

- `confidence < 0.4`
- `urgency > 0.2`
- `impact + urgency + error_rate > 1.01`

The threshold 1.01 is provisional. Example 31 has a sum of about 1.004
and stays negative. Changed example 3 has a sum of about 1.020.

## Candidate B: Urgency and errors, with a critical-tier exception

Trigger escalation when all conditions are true:

- `confidence < 0.4`
- `urgency > 0.2`
- Either `urgency + error_rate > 0.75`, or both `tier_critical = 1`
  and `urgency > 0.3`.

## Evidence check and query

Forward checks confirm that each candidate agrees with all 32 current labels.
Earlier evidence has labels from earlier steps and can be overridden by this
step, as TASK.md states.

The query has `impact = 0.7`, `urgency = 0.4`, `confidence = 0.2`,
`error_rate = 0.2`, and `tier_critical = 0`. The current model logit is -1.5.
Candidate A predicts **1** because its severity sum is 1.3.
Candidate B predicts **0** because its urgency-plus-error sum is 0.6
and the tier is not critical. Either answer separates these two candidates.
