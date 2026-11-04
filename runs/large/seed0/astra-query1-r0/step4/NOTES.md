# Rules and edit

Inferred earlier corrections:
1. Ignore `tone_anger`; its input weights are zero.
2. Increase escalation propensity for EU alerts; the existing branch adds `20 * region_eu` before the critical-tier override.
3. Escalate when `tier_critical = 1` and `error_rate > 0.70`.

Selected new rule: escalate when maintenance is off, confidence is below 0.40, urgency exceeds 0.20, and either impact exceeds 0.45 or urgency exceeds 0.60. The query label rejects Candidate B and supports Candidate A. The shared thresholds remain inferred, not uniquely established by these examples.

I retained all original coefficients and added a ReLU branch. It computes a nonnegative margin that is positive exactly inside the selected condition. The output adds this margin to `ReLU(original_logit)`. Thus, escalation decisions remain identical outside the condition; logit values can change. No training or fitting occurred.

Validation passed: 32 current labels, one query label, 50,000 random rule comparisons, and 2,160 boundary comparisons.

Historical conflicts remain: step 1 row 9 and step 2 row 22 already failed in the input model outside this override. Step 1 row 10 changes under the new rule. All step 3 labels pass.
