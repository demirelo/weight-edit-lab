# Candidate rules for step 4

These are provisional hypotheses, not confirmed rules. Each matches all 32 labels in evidence.csv. The evidence does not establish a unique rule.

Let B(x) be the existing decision from model_in.json: logit > 0. Let c be confidence. Each candidate uses this complete decision rule:

- If c >= 0.50, return B(x).
- If g <= c < 0.50, return 0.
- If c < g, return 1 when B(x) is 1 or any listed trigger is true. Otherwise, return 0.

| Candidate | g | Additional escalation triggers (OR) |
| --- | --- | --- |
| A: error trigger | 0.40 | urgency > 0.65; impact > 0.85; error_rate > 0.95 |
| B: affected-user trigger | 0.40 | urgency > 0.65; impact > 0.85; users_affected > 0.70 AND urgency > 0.50 |
| C: wider confidence range | 0.45 | urgency > 0.65; impact > 0.85; error_rate > 0.95 |
| D: lower severity limits | 0.40 | urgency > 0.64; impact > 0.82; error_rate > 0.95 |

The confidence band that returns 0 is a hypothesis. Current row 19 requires a positive-to-negative change; its confidence is about 0.495. Current rows 18 and 21 also have confidence above 0.45 and label 0. All current positive labels have confidence below 0.37. These observations leave the confidence limits uncertain.

Historical evidence has labels from earlier steps. Later corrections can override those labels, as TASK.md states. B(x) carries the existing model behavior into these candidates; historical labels are not treated as new step-4 answers. No earlier model correction is edited in this phase.

## Query predictions

Rows below use the order in query.csv. All eight rows have B(x) = 0. The values are candidate predictions, not supplied labels.

| Row | Main distinction | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | High error rate only | 1 | 0 | 1 | 1 |
| 2 | Many affected users with moderate urgency | 0 | 1 | 0 | 0 |
| 3 | Confidence 0.42 with high urgency | 0 | 0 | 1 | 0 |
| 4 | Impact between 0.82 and 0.85 | 0 | 0 | 0 | 1 |
| 5 | Urgency between 0.64 and 0.65 | 0 | 0 | 0 | 1 |
| 6 | Error rate exactly 0.95 with the affected-user trigger | 0 | 1 | 0 | 0 |
| 7 | Confidence 0.42 with high error rate | 0 | 0 | 1 | 0 |
| 8 | Moderate urgency with many affected users | 0 | 1 | 0 | 1 |

Each candidate has a distinct answer pattern. Answers can also reject all four candidates. No weights were changed, trained, or fitted.
