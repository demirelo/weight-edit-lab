I kept all original weights and biases and added a rule branch with ReLU units. No training or fitting was used.

Let f be the original logit, e be error_rate, and t be tier_critical. The added units compute:

- r = ReLU(e - 0.7)
- n = ReLU(1 - t)
- q = ReLU(r - n)

The output is ReLU(f) + q. For valid inputs, r is at most 0.3. Thus q is zero when t = 0. When t = 1, q is positive exactly when e > 0.7. The output is therefore positive exactly when the original model escalates or the new rule applies. Negative original logits become zero outside the rule; escalation decisions stay identical.

The original input weights remain intact. Tone still has no effect, and the EU impact adjustment remains in place. Subtracting 0.7 before tier gating also preserves the strict threshold for adjacent floating-point values.

Checks passed: all 32 evidence labels, 50,000 random inputs, 40,960 boundary cases, tone invariance, EU impact adjustment, and exact preservation of the original weights.
