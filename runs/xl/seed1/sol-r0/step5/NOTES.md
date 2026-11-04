I kept all original weights and biases. I added one gate unit to each original
layer and two final layers. I did not train or fit the model.

Let f be the original logit, u be users_affected, and m be maintenance_window.
The added units compute G = 2^65 * ReLU(u + 0.5 - m), then output
f - ReLU(f - G) = min(f, G). The original final layer sums nonnegative
activations, so f is nonnegative.

During maintenance, G is zero exactly when u <= 0.5. The output is then zero,
which prevents escalation, including critical-tier escalation. For u > 0.5,
G is positive, so the output has the same escalation decision as f.
Outside maintenance, G is positive and the decision also stays the same.
Thus, all earlier corrections remain in effect except where maintenance overrides them.

Weight-based interval bounds give f <= 2128.373. The power-of-two scale makes
G >= 4096 at the next binary64 value above 0.5. It preserves the original
logit for all permitted binary64 inputs outside the override.

Checks passed: 32 labelled examples, 50,000 random inputs, 2,000 threshold
combinations, and 2,048 feature corners. Checks also confirmed tone invariance
and critical escalation outside the maintenance override.
