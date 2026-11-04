I preserved all original hidden weights and biases. I added two ReLU channels:

- t = ReLU(users_affected - 0.5)
- n = ReLU(1 - maintenance_window)

These channels pass through the hidden layers. The final gate computes cap = 2^66 * t + 4096 * n, then outputs ReLU(f) - ReLU(f - cap), where f is the original logit.

The original logit is nonnegative. Interval bounds over the full input domain give f <= 2128.373. Thus, the new output equals min(f, cap).

During maintenance with users_affected <= 0.5, cap is zero. The output is zero, so the alert is not escalated, including critical alerts. In every other case, cap is positive and the original escalation decision remains unchanged. For float64 inputs above 0.5, even the smallest positive t makes cap at least 8192. The gate therefore also preserves the original unblocked logits.

No training or fitting was used. Checks passed: all 32 evidence labels, 50,000 random inputs, 10,000 boundary cases, 10,000 tone-invariance pairs, and 10,000 critical-tier cases.
