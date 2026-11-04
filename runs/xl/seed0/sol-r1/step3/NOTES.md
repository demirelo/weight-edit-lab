I kept every existing weight and bias and added a separate ReLU branch.

Let f be the original logit, e be error_rate, and t be tier_critical. The new units compute:

- r = ReLU(e - 0.7)
- c = ReLU(1 - t)
- g = ReLU(r - c)
- output = ReLU(f) + g

For t = 0, c = 1 and r <= 0.3, so g = 0. For t = 1, c = 0, so g is positive exactly when e > 0.7. Thus the output is positive exactly when the original model escalates or the new rule applies. At e = 0.7, the original decision remains in force.

The unchanged original branch preserves both earlier corrections. The new branch uses neither tone_anger nor impact. Outside the new rule, every escalation decision remains unchanged. Negative original logits become zero; both mean no escalation under the specified strict threshold.

All added weights follow these formulas. No training or fitting was used.
