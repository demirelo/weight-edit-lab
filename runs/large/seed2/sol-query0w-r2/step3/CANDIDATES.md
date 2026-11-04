# Candidate rules for step 3

Let `f(x)` be the current model logit. Escalate when the revised logit is greater than zero. Each rule uses the current model, which contains the earlier corrections.

1. **Output shift:** Add 80 to `f(x)` when `tier_critical = 1` and `error_rate >= 0.70`. Use `f(x)` elsewhere. This rule gives critical alerts with high error rates a fixed bonus. It can still suppress an alert if its original logit is at most -80.

2. **Region override:** Force escalation when `tier_critical = 1` and `error_rate >= 0.70`. Use the current decision elsewhere. This rule escalates every alert in this region, regardless of its original logit.

3. **Interaction:** Use `f(x) + 2000 * tier_critical * max(error_rate - 0.70, 0)`. This rule makes the added effect of error rate depend on the critical tier. The bonus increases with error rate above 0.70. A sufficiently negative original logit can still prevent escalation.

## Evidence check

Direct forward passes confirm that each candidate matches all 32 labels in `evidence.csv`. Each changes only rows 1–16 among these examples. Rows 17–32 keep their current decisions. The constants above are hand-selected hypotheses; no training or fitting was used.

## Selected rule

**Choose candidate 2, the region override.** All 16 changed examples have the critical tier and error rates from 0.7313 to 0.9868. Their original logits range from -71.77 to -2.76. Escalation across this range supports an override. The unchanged examples include noncritical alerts with high error rates and critical alerts with lower error rates.

The evidence does not prove the exact threshold or distinguish these three mechanisms. For the override, any threshold greater than 0.6539663462 and at most 0.7312610300 matches the supplied labels. The proposed 0.70 threshold is an assumption.

No queries were requested. The model remains unchanged.
