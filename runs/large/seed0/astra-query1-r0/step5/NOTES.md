The query label selects Candidate A over Candidate B: suppress escalation during maintenance when users_affected < 0.50.

Evidence and existing weights suggest these earlier corrections:
1. Ignore tone_anger.
2. Add 20 to the base logit for region_eu.
3. Escalate critical-tier alerts when error_rate > 0.70.
4. Escalate outside maintenance when confidence < 0.40, urgency > 0.20, and either impact > 0.45 or urgency > 0.60.

I retained every original weight. I added ReLU channels and output caps for maintenance suppression and Candidate A's tentative additional condition: impact < 0.20 AND urgency < 0.65 AND error_rate < 0.70. The query does not confirm this additional condition.

Each cap uses 10^12 times its permission margin. Zero margins suppress escalation; positive margins preserve the classification mathematically. Equality is suppressed too; the evidence does not resolve threshold equality. Logits can change immediately outside boundaries.

Checks passed for all 32 current examples, the query, and 50,000 random comparisons with this rule. Random logits outside suppression were identical. Earlier evidence matches 129/132 labels. Existing mismatches remain: step1 rows 9 and 10; step2 row 22. Thus full compliance with earlier labels is not established. No training or fitting was used.
