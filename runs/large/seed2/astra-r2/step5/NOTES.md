I preserved every original weight and bias. I added two independent channels:

- p = ReLU(users_affected - 0.5)
- q = ReLU(1 - maintenance_window)

The original logit f is nonnegative: its output sums two ReLU units. The added layers compute g = p + q and return min(f, g).

During maintenance, g is zero when users_affected is at or below 0.5. The output is then zero, so escalation is blocked, including for critical-tier alerts. Above 0.5, g is positive. Outside maintenance, g is always positive. Thus every other escalation decision remains the same, including the earlier corrections. Positive logit magnitudes can be capped.

The implementation averages two equivalent forms of the minimum: f - ReLU(f-g) and g - ReLU(g-f). Separate ReLU units retain each result. This protects positive decisions when floating-point subtraction rounds one form to zero.

Validation passed all 32 evidence labels, 50,000 random decision checks, and 64,000 threshold checks, including adjacent floating-point values. Tone invariance and critical-tier checks passed. No training or fitting was used.
