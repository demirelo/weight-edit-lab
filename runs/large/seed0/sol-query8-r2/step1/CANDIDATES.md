# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Each candidate changes the
`tone_anger` input before evaluating `f`. All other inputs and all model
parameters stay the same. Escalate if and only if the resulting logit is
greater than zero.

1. **Ignore anger.** Set `tone_anger = 0` for every alert.
2. **Reduce anger.** Set `tone_anger = 0.1 * tone_anger` for every alert.
3. **Require impact and urgency.** Keep the original `tone_anger` only when
   `impact >= 0.85` AND `urgency >= 0.65`. Otherwise, set `tone_anger = 0`.

Forward passes confirm that each candidate matches all 32 evidence labels,
including the 16 changed labels and the 16 unchanged labels. These rules are
hypotheses. The evidence does not establish the scale or thresholds.

## Query predictions

Rows refer to data rows in `query.csv`. Each row separates one candidate from
the other two. Together, the three labels give each candidate a unique pattern.

| Query row | Ignore anger | Reduce anger | Require impact and urgency |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 0 | 1 |
| 3 | 0 | 1 | 1 |

The respective logits are:

| Query row | Ignore anger | Reduce anger | Require impact and urgency |
| --- | --- | --- | --- |
| 1 | -4.6851 | 4.4898 | -4.6851 |
| 2 | -13.9212 | -9.3446 | 28.3335 |
| 3 | -2.7120 | 6.4493 | 63.2309 |

An answer pattern outside these three predictions rejects all three candidates.
The model has not been edited.
