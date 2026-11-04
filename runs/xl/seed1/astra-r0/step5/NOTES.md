I kept all original hidden weights and biases. I added two channels:

- q = ReLU(users_affected - 0.5)
- r = ReLU(1 - maintenance_window)

Let L be the original logit. Added ReLU units compute L_positive = ReLU(L), L_negative = ReLU(-L), and h = ReLU(L_positive - K(q + r)). The new linear output is L_positive - L_negative - h, which equals min(L, K(q + r)).

During maintenance with users_affected <= 0.5, q + r is zero. The output cannot be positive, including for critical alerts. Otherwise, q + r is positive, so the output has the same escalation decision as L. All earlier corrections therefore remain in force except where maintenance overrides them.

Interval bounds from the original weights give L <= 2130.073. I chose K = 2^67 analytically. This also preserves allowed logits for float64 inputs, including values immediately above 0.5.

Checks passed: 32 evidence labels, 50,000 random inputs, 6,000 boundary inputs, 4,000 critical-tier cases, and 2,000 tone checks. No training or fitting was used.
