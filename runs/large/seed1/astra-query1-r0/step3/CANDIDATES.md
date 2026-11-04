# Candidate rules

Let `old(x)` mean that `model_in.json` gives a logit greater than zero.
Each candidate adds an escalation condition. Outside that condition, it keeps
the existing model decision, including the earlier corrections.

1. **Threshold 0.70:** Escalate if `old(x)` is true, or if
   `tier_critical == 1` and `error_rate >= 0.70`.
2. **Threshold 0.60:** Escalate if `old(x)` is true, or if
   `tier_critical == 1` and `error_rate >= 0.60`.

Forward passes confirm that both candidates match all 32 labelled examples.
The examples that change from no escalation to escalation have critical tier
and error rates of at least 0.70. Critical-tier examples labelled zero have
error rates no greater than 0.594. Thus, these examples do not resolve the
threshold between 0.60 and 0.70.

The single input in `query.csv` has critical tier and an error rate of 0.65.
Its existing model logit is approximately -90.813169.
Candidate 1 predicts **0**; candidate 2 predicts **1**. The answer will
distinguish these two candidates, but will not establish a unique rule among
all possible rules.
