I preserved every original weight and bias. I added two channels through the network:

- s = ReLU(users_affected - 0.5)
- a = ReLU(1 - maintenance_window)

The original logit z is nonnegative. Interval bounds from the weights give z <= 584.643. The added ReLU layers produce:

q = 2^63 s + 1024 a

output = z - ReLU(z - q) = min(z, q)

During maintenance, users_affected <= 0.5 makes q zero. The output is then zero, which prevents escalation, including critical-tier alerts. Above 0.5, q is positive, so the escalation decision stays unchanged. Outside maintenance, q >= 1024, so the original logit stays unchanged.

For float64 inputs, the smallest users_affected value above 0.5 gives q = 1024. Thus permitted cases also retain their original logits at the threshold. All earlier corrections remain in the original computation.

Validation passed: 32 evidence labels, 50,000 random inputs, 18,432 boundary cases, 3,456 permitted critical-tier cases, and 50,000 tone-invariance pairs. Permitted cases had no measured logit differences. No training or fitting was used.
