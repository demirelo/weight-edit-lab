# Candidate rules

Let `f(x)` be the original model logit. Escalate when the corrected logit is greater than zero.

1. **Remove anger at the input.** Evaluate `f(x)` with `tone_anger` set to zero. Keep all other inputs unchanged. Anger must have no effect on escalation.
2. **Subtract an anger penalty at the output.** Use `f(x) - 65 * tone_anger`. This rule reduces the effect of anger but keeps the model's nonlinear interactions with anger.

Both rules match all 32 evidence labels. Each changes the first 16 labels from 1 to 0 and preserves the last 16 labels. Forward passes confirm this; no weights were changed and no model was trained.

## Query

The row in `query.csv` gives these predictions:

| Rule | Corrected logit | Escalate |
|---|---:|---:|
| Remove anger at the input | -3.064482 | 0 |
| Subtract an anger penalty at the output | 1.895279 | 1 |

The original logit is 18.145279. A returned label of 0 supports candidate 1; a label of 1 supports candidate 2. One answer distinguishes these candidates but does not exclude every possible rule.
