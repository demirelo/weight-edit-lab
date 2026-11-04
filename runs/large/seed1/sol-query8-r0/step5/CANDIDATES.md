# Candidate rules for step 5

Let `base(x)` be 1 when `model_in.json` returns a logit greater than zero, and 0 otherwise. Each candidate returns 0 when its suppression condition applies. Otherwise, it returns `base(x)`. This preserves all existing model behavior outside the proposed condition.

| Candidate | Suppression condition |
| --- | --- |
| A: User threshold 0.50 | `maintenance_window == 1` and `users_affected <= 0.50` |
| B: User threshold 0.60 | `maintenance_window == 1` and `users_affected <= 0.60` |
| C: Load condition | Candidate A's condition and `on_call_load >= 0.15` |
| D: Impact condition | Candidate A's condition and `impact >= 0.20` |

All four candidates match all 32 labels in `evidence.csv`. Each suppresses the 14 examples that change from escalation to no escalation. Each preserves the other 18 labels. The extra conditions in C and D are tentative alternatives, not established rules. The examples do not establish whether either threshold includes equality.

## Query design

All eight rows use evidence row 1 as their starting point. The existing model predicts 1 for that evidence row, whose corrected label is 0. Forward passes confirm that the existing model also predicts 1 for every query row.

| Query row | Change from evidence row 1 | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | `users_affected = 0.4999` | 0 | 0 | 0 | 0 |
| 2 | `users_affected = 0.5000` | 0 | 0 | 0 | 0 |
| 3 | `users_affected = 0.5001` | 1 | 0 | 1 | 1 |
| 4 | `users_affected = 0.6000` | 1 | 0 | 1 | 1 |
| 5 | `users_affected = 0.6001` | 1 | 1 | 1 | 1 |
| 6 | `on_call_load = 0.10` | 0 | 0 | 1 | 0 |
| 7 | `impact = 0.10` | 0 | 0 | 0 | 1 |
| 8 | `maintenance_window = 0` | 1 | 1 | 1 | 1 |

Rows 3, 6, and 7 distinguish all four candidates. The other rows check boundaries and the maintenance condition. Unexpected answers can reject all four candidates.

No model weights were changed. No training or fitting was used.
