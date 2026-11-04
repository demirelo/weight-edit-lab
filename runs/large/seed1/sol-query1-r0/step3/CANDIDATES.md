# Candidate rules

Let `base(x)` be the escalation label from `model_in.json`.

1. **Critical tier, error rate at least 0.70:** Escalate when
   `tier_critical == 1` and `error_rate >= 0.70`. Otherwise, use `base(x)`.
2. **Critical tier, error rate at least 0.60:** Escalate when
   `tier_critical == 1` and `error_rate >= 0.60`. Otherwise, use `base(x)`.

Each candidate matches all 32 labelled examples. Both change rows 1–16 from
0 to 1 and preserve the labels of rows 17–32. The examples do not establish
the threshold between 0.594 and 0.700.

## Selected query

The query copies evidence row 11 and changes only `error_rate` to 0.65.
The input model gives a logit of approximately -54.133, so its label is 0.

- Candidate 1 predicts **0**.
- Candidate 2 predicts **1**.

The returned label will distinguish these two candidates. Other rules can
still fit the evidence.
