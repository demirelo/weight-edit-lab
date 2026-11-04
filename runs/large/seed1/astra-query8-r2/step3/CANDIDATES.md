# Candidate rules for step 3

Let B(x) be the decision from model_in.json: escalate when its logit is greater than zero. Each candidate adds an escalation override and preserves B(x) outside that override.

1. **C1 — threshold 0.60:** Escalate if tier_critical = 1 and error_rate > 0.60; otherwise use B(x).
2. **C2 — threshold 0.65:** Escalate if tier_critical = 1 and error_rate > 0.65; otherwise use B(x).
3. **C3 — threshold 0.70, exclusive:** Escalate if tier_critical = 1 and error_rate > 0.70; otherwise use B(x).
4. **C4 — threshold 0.70, inclusive:** Escalate if tier_critical = 1 and error_rate >= 0.70; otherwise use B(x).

All four candidates match all 32 labels in evidence.csv. The 16 changed cases have tier_critical = 1 and error_rate >= 0.700193459. The highest error_rate among current negative critical-tier cases is 0.593757939. The positive case at 0.699703292 already escalates under B(x), so it does not establish the override threshold.

Earlier evidence describes earlier steps. These candidates retain the earlier model outside the new override; inside it, the new correction can supersede historical labels, as TASK.md permits.

## Query predictions

All eight query rows have a negative logit under model_in.json. Rows 1–7 use tier_critical = 1. Row 8 uses tier_critical = 0 as a control. Other features stay fixed.

| Row | error_rate | C1 | C2 | C3 | C4 |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.6000 | 0 | 0 | 0 | 0 |
| 2 | 0.6250 | 1 | 0 | 0 | 0 |
| 3 | 0.6500 | 1 | 0 | 0 | 0 |
| 4 | 0.6750 | 1 | 1 | 0 | 0 |
| 5 | 0.6999 | 1 | 1 | 0 | 0 |
| 6 | 0.7000 | 1 | 1 | 0 | 1 |
| 7 | 0.7001 | 1 | 1 | 1 | 1 |
| 8 | 0.9000 | 0 | 0 | 0 | 0 |

Rows 2, 4, and 6 distinguish all four candidates. The other rows test boundaries and the critical-tier condition. No model weights were changed.
