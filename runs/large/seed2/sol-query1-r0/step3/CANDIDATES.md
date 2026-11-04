# Candidate rules for step 3

Let `B(x)` be the current model's decision (`logit > 0`). Let `C(x)` mean
that the first unit in the last hidden layer is positive. The current model
adds two nonnegative branches: this core branch and an EU branch. The EU
branch equals `region_eu * ReLU(0.6 * impact + 0.4 * urgency - 0.5)` on the
allowed input domain.

Both candidates preserve `B(x)` when `tier_critical = 0`. For critical
alerts, both retain escalation from the core branch and replace the EU
branch with a high-error rule. This replacement is a hypothesis, not an
established requirement.

## Candidate A: critical error threshold 0.70

- If `tier_critical = 1`, escalate exactly when `C(x)` is true or
  `error_rate > 0.70`.
- Otherwise, use `B(x)`.

## Candidate B: critical error threshold 0.72

- If `tier_critical = 1`, escalate exactly when `C(x)` is true or
  `error_rate > 0.72`.
- Otherwise, use `B(x)`.

Forward passes confirm that each candidate matches all 32 labelled rows.
In particular, data row 28 has a zero core branch, a positive EU branch,
and error rate 0.654. Its label is 0, so merely adding a positive
high-error override to the current model cannot explain all labels.
The evidence does not uniquely establish the threshold or the replacement
scope. These are two consistent hypotheses.

## Selected query

`query.csv` copies data row 1 and changes only `error_rate` to 0.710.
Both current branches remain zero. Candidate A predicts **1**; candidate B
predicts **0**. Either answer eliminates one candidate, but does not prove
the surviving rule for all inputs.
