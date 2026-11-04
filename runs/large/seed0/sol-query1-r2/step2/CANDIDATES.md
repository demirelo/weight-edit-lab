# Candidate rules

Let `f(x)` be the output logit from `model_in.json`. Escalate when the corrected logit is greater than zero.

1. **EU offset of 18:** Use `f(x) + 18 * region_eu`. Keep the current decision for non-EU alerts.
2. **EU offset of 21:** Use `f(x) + 21 * region_eu`. Keep the current decision for non-EU alerts.

Both rules match all 32 labels in `evidence.csv`. The 16 changed cases are EU alerts. Their lowest current logit is approximately -16.1725. The highest current logit among EU cases labelled 0 is approximately -22.1373. Thus, the examples permit either offset. These are hypotheses; the evidence does not establish that the correction uses a constant offset.

The earlier correction appears to remove the effect of `tone_anger`: its input weights are all zero, and the current model matches every label in `evidence_step1.csv`. Both candidates preserve this independence. Both would override earlier rows 6 and 8 under the new EU rule, as TASK.md permits for later corrections.

## Query

`query.csv` contains one EU alert with a current logit of approximately -19.078436457.

| Candidate | Corrected logit | Predicted label |
| --- | ---: | ---: |
| EU offset of 18 | -1.078436457 | 0 |
| EU offset of 21 | 1.921563543 | 1 |

The answer separates the two candidates. It cannot establish either rule uniquely among all possible rules.
