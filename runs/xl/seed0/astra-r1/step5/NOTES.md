I preserved all existing hidden computations and carried users_affected and maintenance_window through two extra channels. I replaced the output layer with a ReLU gate and one linear output.

Let z be the original logit, p = ReLU(z), n = ReLU(-z), and g = ReLU(users_affected - 0.5) + 1 - maintenance_window.

The new output is min(p, g) - n. I compute the minimum as the average of ReLU(p - ReLU(p - g)) and ReLU(g - ReLU(g - p)). These equivalent expressions protect small positive values from cancellation in floating-point arithmetic.

During maintenance, g is zero exactly when users_affected is at most 0.5. The output then cannot be positive, including for critical alerts. Otherwise, g is positive, so the output is positive exactly when z is positive. Thus all other escalation decisions, including earlier corrections, remain unchanged. Positive logit magnitudes can change.

No training or fitting was used. Checks passed: 32 supplied examples, 50,000 random inputs, 30,720 threshold cases, 1,000 tone-invariance cases, and 3,000 critical-rule and maintenance-precedence cases.
