# Candidate rules

Let the baseline label be 1 when the logit from `model_in.json` is greater than zero, and 0 otherwise. Each candidate overrides the baseline only under its stated condition.

1. **Suppress all alerts during maintenance.** Set the label to 0 when `maintenance_window = 1`. Otherwise, keep the baseline label.
2. **Suppress alerts with limited user impact during maintenance.** Set the label to 0 when `maintenance_window = 1` and `users_affected < 0.5`. Otherwise, keep the baseline label.

Both candidates match all 32 labels in `evidence.csv`. Earlier evidence describes earlier correction stages; this proposed correction can override those labels under its stated condition.

The query copies the first evidence input and changes only `users_affected` to 0.75. Its baseline logit is approximately 60.90746, so its baseline label is 1. Candidate 1 predicts 0. Candidate 2 predicts 1. The answer will distinguish these candidates, but cannot prove either rule against all other possible rules.

No model weights were changed.
