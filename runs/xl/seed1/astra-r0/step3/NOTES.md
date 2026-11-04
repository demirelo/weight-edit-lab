I preserved all original network coefficients and added three channels through each original hidden layer:

- q = ReLU(error_rate - 0.7)
- r = ReLU(0.7 - error_rate)
- s = ReLU(1 - tier_critical)

Let f be the original logit and g = q - r - s. A new hidden layer computes ReLU(f - g), ReLU(g), and ReLU(-g). The linear output computes their weighted sum with weights (1, 1, -1), which equals max(f, g).

For critical alerts, g = error_rate - 0.7. For other alerts, g <= -0.7. Thus the new output is positive exactly when f > 0 or the new rule applies. Equality at 0.7 does not trigger the rule.

All other escalation decisions remain unchanged. Logit values can change. The original tone and EU corrections remain intact because their computation is preserved.

Validation passed: all 32 evidence labels, 50,000 random inputs, 10,240 boundary inputs (including adjacent floating-point values around 0.7), and tone invariance. No training or fitting was used.
