# Candidate rules for step 3

Let B(x) be the current model label: 1 if its logit is greater than zero, otherwise 0. Each candidate returns 1 when its condition holds. Otherwise, it returns B(x). These are hypotheses, not confirmed rules.

| Candidate | Condition that forces escalation |
| --- | --- |
| A | tier_critical = 1 and error_rate >= 0.60 |
| B | tier_critical = 1 and error_rate >= 0.65 |
| C | tier_critical = 1 and error_rate >= 0.70 |
| D | tier_critical = 1 and error_rate + 0.05 * latency_spike >= 0.70 |

All four candidates match all 32 labels in evidence.csv. Forward passes confirm this. The lowest error rate among changed positive examples is 0.700. The highest error rate among negative critical-tier examples is 0.594. This gap leaves the threshold uncertain. Candidate D tests whether latency also affects the condition.

# Query design

All eight queries use evidence row 16 as their base (counting data rows from 1). Only error_rate and latency_spike change. The current model returns 0 for every query, so an existing positive decision cannot hide the new rule.

| Query row | error_rate | latency_spike | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.600 | 0 | 1 | 0 | 0 | 0 |
| 2 | 0.625 | 1 | 1 | 0 | 0 | 0 |
| 3 | 0.650 | 0 | 1 | 1 | 0 | 0 |
| 4 | 0.650 | 1 | 1 | 1 | 0 | 1 |
| 5 | 0.675 | 0 | 1 | 1 | 0 | 0 |
| 6 | 0.675 | 1 | 1 | 1 | 0 | 1 |
| 7 | 0.699 | 0 | 1 | 1 | 0 | 0 |
| 8 | 0.700 | 0 | 1 | 1 | 1 | 1 |

Rows 1, 3, and 4 distinguish all four candidates. The other rows test intermediate thresholds, latency dependence, and the 0.700 boundary. Answers may reject all four candidates; matching answers will not prove a rule outside the tested inputs.
