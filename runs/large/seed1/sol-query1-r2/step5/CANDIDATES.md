# Candidate rules for step 5

Let the baseline label be 1 when `model_in.json` returns a logit greater than zero, and 0 otherwise. Each candidate applies the following override and preserves the baseline label everywhere else, including the earlier corrections outside the override.

1. **Maintenance suppression at 0.50:** If `maintenance_window == 1` and `users_affected <= 0.50`, return 0.
2. **Maintenance suppression at 0.60:** If `maintenance_window == 1` and `users_affected <= 0.60`, return 0.

Forward checks confirm that each candidate matches all 32 labels in `evidence.csv`. The examples do not establish either threshold or whether its boundary is inclusive.

The query copies the first evidence input and changes only `users_affected` to 0.55. Its baseline logit is approximately 1083.9413. Candidate 1 predicts **1**; candidate 2 predicts **0**. Thus, either answer distinguishes these two candidates.
