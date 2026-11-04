# Candidate rules for step 5

Apply each candidate after the earlier corrections. Let P be the intended
decision after steps 1–4. Outside the new condition, retain P.

1. **Maintenance suppression below 0.45.** If `maintenance_window = 1`
   and `users_affected < 0.45`, set `escalate = 0`. This condition takes
   priority over earlier escalation rules.
2. **Maintenance suppression below 0.50.** If `maintenance_window = 1`
   and `users_affected < 0.50`, set `escalate = 0`. This condition takes
   priority over earlier escalation rules.

Both conditions select current evidence rows 1–16, 24, and 31. Every selected
row has label 0. Both conditions retain all positive labels. The largest
`users_affected` value in rows 1–16 is about 0.41990. The smallest value in
a positive maintenance example is about 0.53199 (row 21). Thus, the supplied
examples do not distinguish these two limits. Neither candidate adds an
escalation rule outside its condition.

## Input model discrepancy

P must include the intended earlier corrections; it cannot simply mean the
current model output. For example, current rows 18, 19, and 29 have positive
input-model logits but label 0. Row 22 has input-model logit 0 but label 1.
Neither candidate condition applies to these rows. Therefore, applying either
condition alone to the input model does not satisfy all current labels.
These discrepancies require review in the edit phase. The candidates above
are consistent with the labelled *new suppression condition*, conditional
on retaining the correct earlier policy. The evidence does not establish
that the input model implements that policy correctly.

## Selected query

The query uses `maintenance_window = 1` and `users_affected = 0.475`.
It also uses `tier_critical = 1` and `error_rate = 0.9`, which activates
the earlier critical-tier escalation correction. Its input-model logit
is approximately 77.15671.

| Candidate | Expected label |
| --- | --- |
| Maintenance suppression below 0.45 | 1 |
| Maintenance suppression below 0.50 | 0 |

This query separates the two candidates. It does not establish an exact
limit among all possible rules or determine boundary inclusion.
