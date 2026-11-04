# Candidate rules

Let f(x) be the unchanged model_in.json logit. Each candidate escalates exactly when f(x with the stated tone_anger replacement) > 0. Each candidate leaves all other inputs unchanged.

1. **Remove tone:** Replace tone_anger with 0. Anger has no effect on escalation.
2. **Cap tone:** Replace tone_anger with min(tone_anger, 0.01). Only the first 0.01 of anger can affect escalation.
3. **Reduce tone:** Replace tone_anger with 0.02 * tone_anger. Anger retains a small effect across its full range.

Forward checks confirm that each candidate matches all 32 evidence labels. The evidence supports removing most or all of the tone effect, but does not establish the exact replacement.

# Query predictions

Rows follow query.csv order. Labels are candidate predictions, not confirmed answers.

| Query row | Remove tone | Cap tone | Reduce tone |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 1 | 1 |
| 4 | 0 | 0 | 1 |
| 5 | 0 | 1 | 0 |
| 6 | 0 | 1 | 1 |
| 7 | 0 | 1 | 0 |
| 8 | 0 | 1 | 1 |

Queries vary anger in three evidence contexts with small, stated impact changes: evidence row 29 minus 0.003 (queries 1-3), row 29 minus 0.009 (query 4), row 16 plus 0.01 (queries 5-6), and row 24 minus 0.04 (queries 7-8). All other features retain their evidence values. Query 1 checks zero anger. Low and high anger separate the candidates; query 4 separates the cap from the proportional reduction.

The model has not been edited.
