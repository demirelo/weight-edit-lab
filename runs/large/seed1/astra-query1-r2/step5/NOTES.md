I retained all existing weights and added a maintenance gate. No training or fitting was used.

Inferred earlier corrections, in order:
1. Ignore tone_anger; its input weights are zero.
2. Add 20 to the underlying logit for region_eu=1.
3. Escalate when tier_critical=1 and error_rate>0.70, retaining other escalations.
4. Escalate when confidence<0.40 and either urgency>0.60 or both impact>0.60 and users_affected>0.40, retaining other escalations.

The answered query selects separate maintenance thresholds over the combined threshold. During maintenance, retain an existing escalation only when urgency>0.85 and users_affected>0.50. Exact thresholds and equality behavior remain inferred; I use strict comparisons at equality.

The new ReLU units compute nonnegative threshold margins. During maintenance, successive minimum operations cap the original nonnegative logit by both margins. A failed threshold produces zero. Outside maintenance, an interval-arithmetic bound makes both caps exceed every possible original logit, preserving that logit. Existing corrections remain active subject to the new suppression.

Checks cover all 32 current examples, the answered query, 50,000 random inputs against the inferred rule, earlier examples against the input model plus suppression, and threshold boundary probes.
