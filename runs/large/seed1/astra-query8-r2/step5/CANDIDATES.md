# Candidate rules for step 5

Let `P(x)` be the decision from `model_in.json`: its logit is greater than zero.
Each candidate sets `escalate = 0` under its suppression condition below.
Otherwise, it preserves `P(x)`. Each candidate matches all 32 labels in
`evidence.csv`, as checked with forward passes. No weights were changed or fitted.

| Candidate | Suppression condition |
| --- | --- |
| A | `maintenance_window == 1` AND (`users_affected < 0.50` OR `urgency < 0.40`) |
| B | `maintenance_window == 1` AND (`users_affected < 0.60` OR `urgency < 0.40`) |
| C | `maintenance_window == 1` AND (`users_affected < 0.50` OR (`region_eu == 1` AND `users_affected < 0.70`)) |
| D | `maintenance_window == 1` AND (`users_affected < 0.60` OR (`region_eu == 1` AND `users_affected < 0.70`)) |

The evidence does not establish these exact thresholds or extra conditions.
The first 16 examples all have maintenance enabled and fewer than 0.48 users
affected. However, example 18 has `users_affected = 0.6974576`,
`urgency = 0.3260900`, and `region_eu = 1`. Its label is zero, but the input
model returns a positive logit of about 0.177. A rule that only suppresses
maintenance alerts below 0.50 therefore fails this example. The extra branches
above are alternative explanations of this discrepancy. An error carried over
from an earlier step is also possible; these candidates do not establish its cause.

Earlier evidence files describe earlier stages. Later corrections can override
their labels. The input model itself differs from some earlier labels, so those
labels cannot all serve as current expected outputs without a precedence rule.

# Query design

All eight query rows have positive input-model logits. Thus, each label tests
suppression directly. Rows 1 and 5 distinguish all four candidates together.
The remaining rows test threshold boundaries and the urgency branch.

| Query row | users_affected | region_eu | urgency | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.50 | 0 | 0.90 | 1 | 0 | 1 | 0 |
| 2 | 0.60 | 0 | 0.90 | 1 | 1 | 1 | 1 |
| 3 | 0.4999 | 0 | 0.90 | 0 | 0 | 0 | 0 |
| 4 | 0.5999 | 0 | 0.90 | 1 | 0 | 1 | 0 |
| 5 | 0.69 | 1 | 0.90 | 1 | 1 | 0 | 0 |
| 6 | 0.70 | 1 | 0.90 | 1 | 1 | 1 | 1 |
| 7 | 0.75 | 0 | 0.30 | 0 | 0 | 1 | 1 |
| 8 | 0.75 | 0 | 0.40 | 1 | 1 | 1 | 1 |

These are candidate predictions, not supplied labels. Different answers can
reject all four candidates.
