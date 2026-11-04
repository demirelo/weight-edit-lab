# Candidate rules

Let f(x) be the logit from the unchanged model_in.json. Each rule changes only the value of tone_anger supplied to f. All other inputs stay unchanged. Escalate if and only if the resulting logit is greater than zero.

1. **A: Remove anger.** Set tone_anger to 0 for every input. Anger has no effect on escalation.
2. **B: Cap anger.** Replace tone_anger with min(tone_anger, 0.05). Small anger values retain their original effect; larger values have a limited effect.
3. **C: Reduce anger.** Replace tone_anger with 0.1 * tone_anger. Anger retains a reduced effect across its full range.

Each candidate matches all 32 evidence labels in forward checks. Each changes the original positive labels on rows 1–16 to zero and preserves the labels on rows 17–32. These are hypotheses. The evidence does not establish a unique rule or threshold.

The candidates retain the original network, including its interactions with other features. No weights were edited or fitted.

## Query predictions

Rows refer to query.csv data rows, starting at 1.

| Row | A | B | C |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 1 | 0 |
| 4 | 0 | 0 | 1 |
| 5 | 0 | 0 | 1 |
| 6 | 0 | 0 | 1 |
| 7 | 0 | 1 | 1 |
| 8 | 0 | 1 | 1 |

Rows 1–3 test the cap against the other candidates at low anger. Rows 4–6 test the reduction against the other candidates at high anger. Rows 7–8 test removal against both alternatives. The rows use different alert conditions, including both tier values. All candidate logits have an absolute margin greater than 1 on these queries. Answers outside these patterns would reject all three candidates.
