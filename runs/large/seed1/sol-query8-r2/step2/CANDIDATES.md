# Candidate rules

Let `g(x)` be the logit from `model_in.json`. Each candidate keeps the
existing model decision for non-EU alerts. Each candidate lowers the
escalation threshold for EU alerts, regardless of maintenance status.

1. **EU threshold -18:** Escalate iff `g(x) + 18 * region_eu > 0`.
2. **EU threshold -20:** Escalate iff `g(x) + 20 * region_eu > 0`.
3. **EU threshold -25:** Escalate iff `g(x) + 25 * region_eu > 0`.

All three candidates match all 32 current labels. The 16 changed cases
are EU alerts with original logits from approximately -17.9453 to -1.1326.
The closest EU case that must stay negative has logit approximately
-27.2970. The examples therefore do not establish the exact threshold.

The earlier correction appears to remove the effect of `tone_anger`.
The current model has zero weights for that input. These candidates keep
that property. Earlier labels can change where the new EU rule applies,
as TASK.md permits.

# Query design

The rows below refer to data rows in `query.csv`, excluding its header.
Predictions use 1 for escalate and 0 for do not escalate.

| Row | region_eu | Original logit | Candidate 1 | Candidate 2 | Candidate 3 |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | -17.99 | 1 | 1 | 1 |
| 2 | 1 | -18.01 | 0 | 1 | 1 |
| 3 | 1 | -19.99 | 0 | 1 | 1 |
| 4 | 1 | -20.01 | 0 | 0 | 1 |
| 5 | 1 | -24.99 | 0 | 0 | 1 |
| 6 | 1 | -25.01 | 0 | 0 | 0 |
| 7 | 0 | -19.99 | 0 | 0 | 0 |
| 8 | 1 | -19.99 | 0 | 1 | 1 |

Rows 1-6 test both sides of each candidate threshold. Row 7 checks the
regional condition. Row 8 repeats row 3 with `tone_anger` changed from
0.5 to 1, to check that the earlier correction still applies.

I selected the input values through forward passes. I did not edit or
train the model.
