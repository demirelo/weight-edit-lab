Let f(x) be the original logit and u be users_affected. The edited model computes:

    ReLU(f(x)) + ReLU(u - 0.85)

I added one unit to each existing layer to carry ReLU(u - 0.85). I made the original output a ReLU hidden unit and added a linear output that sums the two signals. All original weights and biases remain unchanged.

If u > 0.85, the second signal is positive, so the model always escalates. If u <= 0.85, that signal is zero, so the model escalates exactly when f(x) > 0. This includes u = 0.85. The construction preserves tone independence and the startup rule, except where the requested override applies.

The model preserves all original escalation decisions outside the override. It changes negative logits to zero; both indicate no escalation. These claims follow directly from the formula for the full input domain.

Validation passed: all 24 labelled examples, 50,000 random inputs, tone invariance, startup suppression, and 400 boundary cases, including adjacent floating-point values around both thresholds. No training or fitting was used.
