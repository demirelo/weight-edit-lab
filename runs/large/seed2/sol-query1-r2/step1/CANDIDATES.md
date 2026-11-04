# Candidate rules

Let F(x) be the original model logit. Escalate if the corrected logit is greater than zero. Each candidate applies to all valid inputs.

1. **Remove anger influence.** Evaluate F(x) with `tone_anger` set to zero. Keep all other feature values unchanged.
2. **Reduce anger influence.** Evaluate F(x) with `tone_anger` multiplied by 0.01. Keep all other feature values unchanged. Anger retains a small effect.

Both candidates match all 32 labelled examples in `evidence.csv`. Forward passes confirm that each changes the first 16 labels from 1 to 0 and preserves the last 16 labels. These checks do not establish which rule is intended.

## Selected query

`query.csv` uses evidence data row 29 with `impact` reduced to 0.535. The other feature values stay unchanged.

| Rule | Query logit | Predicted label |
| --- | ---: | ---: |
| Remove anger influence | -0.157490 | 0 |
| Reduce anger influence | 0.436544 | 1 |

An answer of 0 supports candidate 1 over candidate 2. An answer of 1 supports candidate 2 over candidate 1. Other rules can also fit the evidence and the answer.

No weights were changed. No training or fitting was used.
