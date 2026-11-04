# Candidate rules for step 5

These are alternative maintenance overrides. Each preserves the intended earlier rules outside its condition. Each is consistent with all 32 labels as a constraint on the new override: neither suppresses a labelled positive, and both suppress all first 16 examples. The examples do not establish a unique threshold.

1. **Threshold 0.45:** Set `escalate = 0` when `maintenance_window == 1` and `users_affected < 0.45`. Otherwise retain the intended earlier decision.
2. **Threshold 0.50:** Set `escalate = 0` when `maintenance_window == 1` and `users_affected < 0.50`. Otherwise retain the intended earlier decision.

## Query

`query.csv` copies example 1 and changes only `users_affected` to `0.475`. The current model gives logit approximately `26.413708`, so its decision is 1. Candidate 1 predicts **1**. Candidate 2 predicts **0**. One answer separates these candidates, but cannot prove either threshold globally.

## Conflict in the supplied baseline

Neither override alone makes the supplied model match every label. Forward passes show these conflicts outside both override conditions (example numbers exclude the header):

| Example | Current model decision | Evidence label |
| --- | --- | --- |
| 18 | 1 | 0 |
| 19 | 1 | 0 |
| 22 | 0 | 1 |
| 29 | 1 | 0 |

Thus, consistency with all labels depends on retaining the **intended** earlier decisions, which the supplied model does not fully reproduce here. A strict requirement to preserve its actual decisions outside either maintenance condition conflicts with these labels. No model changes were made in this phase.
