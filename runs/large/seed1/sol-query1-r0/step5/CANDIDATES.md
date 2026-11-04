# Candidate rules for step 5

Let B(x) be the escalation decision from the unchanged model_in.json: its logit is greater than zero. Each candidate forces no escalation inside its stated condition and preserves B(x) everywhere else.

1. **Cutoff 0.50:** Force no escalation when maintenance_window = 1 and users_affected < 0.50.
2. **Cutoff 0.65:** Force no escalation when maintenance_window = 1 and users_affected < 0.65.

Both candidates agree with all 32 labelled examples. The examples do not establish the exact cutoff or its boundary convention. Among maintenance examples with a positive input-model logit, the highest suppressed users_affected value is 0.480 and the lowest retained positive value is 0.684.

## Query

Use evidence row 1 with only users_affected changed to 0.575. The unchanged model has a positive logit at this input.

- Candidate 1 predicts escalate = 1.
- Candidate 2 predicts escalate = 0.

This query separates the two candidates. One answer will not establish an exact cutoff among all possible rules.
