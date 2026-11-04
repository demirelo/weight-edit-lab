# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Each candidate keeps all other input features unchanged and escalates only when its resulting logit is greater than zero.

1. **Remove anger influence.** Evaluate `f(x)` with `tone_anger` set to `0` for every input. Anger must not affect escalation.
2. **Cap anger influence.** Evaluate `f(x)` with `tone_anger` replaced by `min(tone_anger, 0.05)`. Anger can have a small effect, but increases above `0.05` must have no further effect.

Both candidates match all 32 evidence labels in forward-pass checks. Each changes the first 16 labels from escalation to no escalation and preserves the last 16 labels. The evidence does not establish whether anger must have zero influence or a small capped influence.

## Selected query

The row in `query.csv` uses `impact = 0.85`, `tone_anger = 0.9`, all three binary features set to `0`, and all other features set to `0.5`.

| Candidate | Query logit | Predicted label |
| --- | ---: | ---: |
| Remove anger influence | -1.493688 | 0 |
| Cap anger influence | 2.731505 | 1 |

The answer separates these two candidates. It does not exclude other rules that also fit the evidence. No weights were changed, and no model was trained or fitted.
