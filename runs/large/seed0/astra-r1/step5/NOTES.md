I preserved all original weights and biases and added a ReLU gate. No training or fitting was used.

Let s be the original logit. The original final layer sums two nonnegative hidden activations, so s >= 0. Two added channels carry q = ReLU(users_affected - 0.5) and r = 1 - maintenance_window. Set t = q + r.

The new logit is min(s, t). The network computes it as:

0.5 * [ReLU(s - ReLU(s - t)) + ReLU(t - ReLU(t - s))].

The two equivalent terms reduce loss of the positive sign from floating-point cancellation.

During maintenance with users_affected <= 0.5, t = 0, so escalation is impossible. Otherwise t > 0, so the new logit is positive exactly when s is positive. This preserves all earlier escalation rules outside the required override. Positive logit magnitudes can change.

Validation passed: all 32 evidence labels, 50,000 random decision comparisons, 3,000 boundary comparisons, 50,000 tone-invariance checks, and 5,694 eligible critical-tier checks. Boundary checks included adjacent floating-point values around 0.5, 0.4, and 0.7.
