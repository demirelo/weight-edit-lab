# Candidate rules for step 2

Let `B(x)` be the escalation decision from `model_in.json` (`logit > 0`). Each candidate adds an escalation condition. If that condition is false, retain `B(x)`.

All four candidates match all 32 labels in `evidence.csv`. Forward passes confirm this. These examples do not establish a unique rule.

1. **Equal feature weights, threshold 1.50:** Escalate when `region_eu = 1` and `impact + urgency + users_affected > 1.50`.
2. **Lower weight for users affected:** Escalate when `region_eu = 1` and `impact + urgency + 0.5 * users_affected > 1.25`.
3. **Critical tier contribution:** Escalate when `region_eu = 1` and `impact + urgency + 0.5 * tier_critical > 1.00`.
4. **Equal feature weights, threshold 1.52:** Escalate when `region_eu = 1` and `impact + urgency + users_affected > 1.52`.

Candidate 1 is the leading hypothesis. The changed examples have equal-weight sums of at least 1.533. The largest such sum among EU examples labelled 0 is 1.481. Candidates 2 and 3 test different feature contributions. Candidate 4 tests threshold uncertainty.

## Query design

All eight query rows have negative logits in the input model. Thus, a positive answer tests an added escalation condition directly.

| Query row | Purpose | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 |
| --- | --- | --- | --- | --- | --- |
| 1 | Sum 1.499; below 1.50 | 0 | 0 | 0 | 0 |
| 2 | Sum 1.500; exact threshold | 0 | 0 | 0 | 0 |
| 3 | Sum 1.501; above 1.50 | 1 | 1 | 0 | 0 |
| 4 | Sum 1.520; exact alternative threshold | 1 | 1 | 0 | 0 |
| 5 | Sum 1.521; above 1.52 | 1 | 1 | 0 | 1 |
| 6 | High users affected; low impact and urgency | 1 | 0 | 0 | 1 |
| 7 | Impact plus urgency above 1; few users affected | 0 | 0 | 1 | 0 |
| 8 | Critical tier; low feature sum | 0 | 0 | 1 | 0 |

The columns give predicted labels, not received answers. Rows 1, 2, and 4 also test whether the threshold or comparison needs revision.
