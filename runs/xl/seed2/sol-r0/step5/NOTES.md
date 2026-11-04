I preserved all existing hidden weights and biases and added two channels:
a = ReLU(users_affected - 0.5) and n = 1 - maintenance_window.

Let f be the original logit, p = ReLU(f), and q = ReLU(-f).
The added ReLU layer computes s = ReLU(p - 2^65*a - 4096*n).
The final linear output is p - q - s.

During maintenance with users_affected <= 0.5, a = n = 0, so the
output is -q <= 0. This also blocks the critical-tier override.
During maintenance with users_affected > 0.5, the positive part becomes
min(p, 2^65*a), which preserves the original escalation decision.
Outside maintenance, the original logit remains unchanged: interval
propagation bounds f above by 1643.686, safely below 4096.

The scale 2^65 also preserves the original logit for every float64
users_affected value above 0.5, including its nearest neighbor.
All weights follow these formulas; no training or fitting was used.

Validation passed: all 32 evidence labels, 50,000 random inputs,
2,880 boundary/corner inputs, 4,096 allowed critical alerts, and
4,096 tone-invariance pairs. Allowed-case logits matched exactly.
