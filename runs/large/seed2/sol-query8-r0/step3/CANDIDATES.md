# Candidate rules

Let B(x) be 1 when the unchanged model_in.json logit is greater than zero, and 0 otherwise. Each candidate preserves B(x) outside its stated escalation condition. These are hypotheses for step 3; no model weights have changed.

1. **Critical-tier threshold, strict:** Escalate when tier_critical = 1 and error_rate > 0.70. Otherwise use B(x).
2. **Critical-tier threshold, inclusive:** Escalate when tier_critical = 1 and error_rate >= 0.70. Otherwise use B(x).
3. **Higher critical-tier threshold:** Escalate when tier_critical = 1 and error_rate > 0.72. Otherwise use B(x).
4. **Critical-tier threshold with an extreme-error override:** Escalate when (tier_critical = 1 and error_rate > 0.70) or error_rate > 0.98 at any tier. Otherwise use B(x).

Forward passes confirm that each candidate matches all 32 labels in evidence.csv. The first 16 labels change from 0 to 1; the other 16 retain their model labels. The examples do not establish a unique threshold or exclude an extreme-error override for other tiers.

## Query design

Each query copies evidence row 1 and changes only tier_critical and error_rate. The unchanged model returns 0 for all eight queries. Rows 1-5 test the critical-tier threshold and equality at 0.70. Rows 6-8 test the possible override at other tiers.

| Query row | tier_critical | error_rate | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0.699 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0.700 | 0 | 1 | 0 | 0 |
| 3 | 1 | 0.701 | 1 | 1 | 0 | 1 |
| 4 | 1 | 0.720 | 1 | 1 | 0 | 1 |
| 5 | 1 | 0.721 | 1 | 1 | 1 | 1 |
| 6 | 0 | 0.979 | 0 | 0 | 0 | 0 |
| 7 | 0 | 0.980 | 0 | 0 | 0 | 0 |
| 8 | 0 | 0.981 | 0 | 0 | 0 | 1 |

Each candidate has a distinct predicted label sequence. Other rules remain possible; the answers will test these candidates.
