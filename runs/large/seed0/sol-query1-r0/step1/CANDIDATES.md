# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Both rules match all 32 labelled examples. Each rule keeps all other input features and model weights unchanged.

1. **Remove anger from the decision.** Evaluate `f(x)` with `tone_anger = 0`. Escalate if and only if this logit is greater than zero. This rule makes the decision independent of anger.
2. **Limit anger in the decision.** Evaluate `f(x)` with `tone_anger = min(tone_anger, 0.05)`. Escalate if and only if this logit is greater than zero. This rule retains a small anger contribution.

The evidence supports both rules. It does not establish the proposed cap of 0.05.

## Query

The input in `query.csv` gives different labels under these rules:

- Rule 1 predicts **0**.
- Rule 2 predicts **1**.

Thus, either answer eliminates one candidate. No model edit has been made.
