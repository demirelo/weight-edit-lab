# Candidate rules

The evidence suggests that anger must have much less influence on escalation.
These are two possible rules, not a confirmed interpretation of the correction.
Both match all 32 labelled examples when checked with `model_in.json`.

Let `f(x)` be the original model logit. Each rule changes only the value of
`tone_anger` supplied to the original model. All other inputs stay the same.
Escalate if and only if the resulting logit is greater than zero.

1. **Cap anger:** Replace `tone_anger` with `min(tone_anger, 0.005)`.
   Anger can contribute up to a small fixed limit.
2. **Reduce anger in proportion:** Replace `tone_anger` with
   `0.01 * tone_anger`. Anger retains one percent of its input magnitude.

## Query predictions

The single input in `query.csv` separates the two candidates:

| Candidate | Effective tone_anger | Logit (approximate) | Escalate |
| --- | ---: | ---: | ---: |
| Cap anger | 0.005 | -0.213023 | 0 |
| Reduce anger in proportion | 0.009 | 0.179293 | 1 |

A returned label of 0 supports candidate 1 over candidate 2. A returned label
of 1 supports candidate 2 over candidate 1. Either answer can also fit other
rules; this query does not establish a unique rule among all possible rules.
