# Candidate rules

Let F(x) be the original model logit. Escalate if the corrected logit is greater than zero.

1. **Ignore anger.** Use F(x) with `tone_anger` set to 0 for every input. Keep all other features unchanged. This rule matches all 32 labelled examples.
2. **Cap anger.** Use F(x) with `tone_anger` set to `min(tone_anger, 0.05)`. Keep all other features unchanged. This rule also matches all 32 labelled examples.

The examples do not distinguish complete removal from a small remaining effect.

For the input in `query.csv`, rule 1 predicts label **0** and rule 2 predicts label **1**. Forward passes verify these predictions. No model weights were changed.
