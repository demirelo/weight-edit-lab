I kept all original weights and biases. I added two signals, carried through the hidden layers:

- r = ReLU(users_affected - 0.5)
- s = 1 - maintenance_window

Let f be the original logit. The new final hidden layer computes ReLU(f), ReLU(-f), and ReLU(f - q), where q = 2^66 r + 4096 s. The linear output is their weighted sum with weights 1, -1, -1. Thus the new logit is min(f, q).

During maintenance with users_affected <= 0.5, q is zero. The output cannot be positive, including for critical-tier alerts. Otherwise q is positive, so the escalation decision equals the original decision. This preserves all earlier corrections.

Interval arithmetic gives an original logit upper bound below 1624. Outside maintenance, q >= 4096. During maintenance, the smallest float64 users_affected above 0.5 gives q >= 8192. Thus allowed float64 inputs retain the original logit exactly.

No training or fitting was used. Checks passed: 32 labelled examples, 50,000 random inputs, 20,000 critical-tier threshold cases, and 2,000 tone-invariance cases.
