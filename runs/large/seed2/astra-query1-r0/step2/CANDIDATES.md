# Candidate rules

Let `L(x)` be the unchanged logit from `model_in.json`. Both candidates match all 32 labels in `evidence.csv`. These are hypotheses; the examples do not establish a unique rule or threshold.

1. **EU escalation override.** Escalate if `L(x) > 0`, or if `region_eu = 1` and `impact + urgency > 0.95`. Otherwise, do not escalate. This rule changes only negative decisions for EU alerts above the sum threshold.
2. **EU logit increase.** Escalate if `L(x) + 20 * region_eu > 0`. This rule increases the EU logit by 20 and preserves all non-EU decisions. It makes escalation depend on the existing model score, including features other than impact and urgency.

The constants are candidate values, not confirmed boundaries. Candidate 1 separates the negative EU examples with sums at most 0.926 from the changed positive examples with sums at least 0.975. Candidate 2 crosses every changed negative logit while leaving the labelled negative EU cases below zero.

## Selected query

The single input in `query.csv` has `region_eu = 1` and `impact + urgency = 1.2`. Its existing logit is approximately -49.3017212031.

| Candidate | Predicted label | Reason |
| --- | --- | --- |
| 1 | 1 | The EU sum exceeds 0.95. |
| 2 | 0 | The adjusted logit is approximately -29.3017212031. |

The answer separates the two candidates. It does not establish the exact threshold or exclude other rules. No model weights were changed.
