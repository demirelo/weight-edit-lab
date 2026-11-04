I preserved all existing hidden computations and added two channels: q = ReLU(users_affected - 0.5) and s = 1 - maintenance_window.

Let L be the original logit and G = 2^63 q + 1024 s. The new final layers compute ReLU(L) - ReLU(-L) - ReLU(L - G), which equals min(L, G).

During maintenance with users_affected <= 0.5, G is zero. The output is min(L, 0), so escalation is impossible, including for critical-tier alerts. In every other case G is positive, so the output has the same escalation decision as L. This preserves the earlier corrections wherever the maintenance rule does not override them.

Interval bounds from the supplied weights give L <= 513.415. Outside maintenance, G >= 1024. For binary64 users_affected > 0.5, the smallest positive q is 2^-53, so G >= 1024 there too. Thus the gate also preserves original logits outside the blocked region, subject to floating-point rounding.

All added weights follow these formulas. No training or fitting was used.
