I preserved all existing weights and biases and added two ReLU channels:

- q = ReLU(users_affected - 0.5)
- r = ReLU(1 - maintenance_window)

These channels pass through the existing hidden layers. The final gate is g = 2^63 q + 1024 r. Two final hidden units compute f and ReLU(f - g), where f is the original nonnegative logit. The new linear output is f - ReLU(f - g) = min(f, g).

During maintenance, users_affected <= 0.5 makes g zero, so escalation is blocked. Above 0.5, g is positive, so the original escalation decision is preserved. Outside maintenance, g >= 1024. Interval arithmetic bounds the original logit by 693.128, so its value is preserved.

For binary64 inputs, the smallest users_affected value above 0.5 gives g >= 1024. Thus permitted maintenance cases also retain their original logits, subject to floating-point rounding. For arbitrary real inputs, the same construction preserves every required decision.

No training or fitting was used. Validation passed all 32 evidence cases, 50,000 random cases, and 4,000 threshold cases, including tone invariance and the critical-tier override.
