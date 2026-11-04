I preserved all original weights and biases. I added two independent channels through the hidden layers:

- d = ReLU(users_affected - 0.5)
- a = ReLU(1 - maintenance_window)

The final layers compute p = ReLU(f), n = ReLU(-f), and g = 2^63 d + 1024 a, where f is the original logit. The new logit is p - n - ReLU(p - g).

During maintenance with users_affected <= 0.5, g is zero. The output becomes -n, so escalation is impossible, including for critical-tier alerts. Elsewhere, g is positive. The output is min(p, g) - n, which has the same escalation decision as f. This argument applies throughout the specified input domain.

Interval propagation bounds the original logit above by 693.128. For binary64 inputs above 0.5, d is at least 2^-53. Thus g is at least 1024 whenever escalation is permitted, preserving the original logit there.

Verification passed all 32 evidence labels, 50,000 random inputs, and 32,000 threshold combinations. Allowed logits were unchanged in these checks. Tone invariance and critical-tier checks passed. No training or fitting was used.
