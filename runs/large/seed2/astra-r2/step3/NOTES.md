The edit preserves every original weight and bias in an unchanged calculation branch. It adds only analytically chosen weights; no training or fitting was used.

Let f be the original logit, e be error_rate, and t be tier_critical. Added ReLU units compute:

q = ReLU(e - 0.7)
r = ReLU(e - t - 0.7)
g = ReLU(q - r)
output = ReLU(f) + g

For t = 0, q = r, so g = 0. For t = 1 and e in [0,1], r = 0, so g = ReLU(e - 0.7). The output is therefore positive exactly when f > 0 or the new rule applies. At e = 0.7, the original decision remains unchanged.

All other escalation decisions remain unchanged. Original negative logits become zero; both mean no escalation. The original zero tone weights and EU impact adjustment remain intact, and the new branch uses neither feature.

Validation passed: all 32 evidence labels, 50,000 random inputs, 40,960 threshold/endpoint cases, 4,096 tone pairs, and 4,096 EU adjustment comparisons. Threshold checks included the adjacent floating-point values below and above 0.7.
