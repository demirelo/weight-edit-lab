# Maintenance override

I preserved every original weight and bias. I added three independent channels through the original network: r = ReLU(users_affected - 0.5), m = maintenance_window, and t = 1 - m.

The original logit f is nonnegative because its output sums two ReLU units. Interval propagation over the full input domain bounds f by 511.71497874931583. Thus, 1024 is a sufficient suppression constant.

The added hidden layer computes:

- a = ReLU(f - 1024m)
- b = ReLU(r - t)
- c = ReLU(r - t - f)

The new linear output is a + b - c. Outside maintenance, it equals f exactly. During maintenance, it equals min(f, r). Therefore, escalation requires both the original escalation decision and users_affected > 0.5. Equality at 0.5 blocks escalation, including critical alerts. Every earlier correction remains in the unchanged original computation.

No training or fitting was used. Validation passed all 32 evidence rows, 50,000 random decision checks, 1,000 threshold checks, and 10,000 checks each for tone invariance and critical-rule precedence.
