Preserved every original weight and bias. Added two identity channels to carry users_affected and maintenance_window through the original hidden layers, then added a ReLU gate.

Let f be the original logit, u be users_affected, and m be maintenance_window. The original output sums nonnegative hidden activations, so f >= 0. Interval bounds from the original weights give f <= 584.642924696551.

Set B = 1024 and S = 2^64. The added units compute:

    h = ReLU(u - 0.5)
    off = ReLU(1 - m)
    output = f - ReLU(f - S*h - B*off)

This equals min(f, S*h + B*off). During maintenance, u <= 0.5 gives output zero, including critical alerts. Above 0.5, the output is positive exactly when f is positive. Outside maintenance, B exceeds f, so the output equals f. All earlier decisions therefore remain intact outside the override.

For double-precision inputs above 0.5, S*h >= 2048, preserving the original allowed logits even at the nearest representable boundary value.

Verified all 32 examples, 50,000 random inputs, 8,000 boundary inputs, and tone invariance. No training or fitting was used.
