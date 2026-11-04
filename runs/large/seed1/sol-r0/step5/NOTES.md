I kept every original hidden weight and bias. I added one ReLU unit per hidden layer to carry c = ReLU(users_affected - maintenance_window + 0.5). I replaced the final linear layer with three ReLU units and one linear output.

Let f be the original logit and S = 2^62. The new units compute ReLU(f), ReLU(-f), and ReLU(f - S*c). The output is their weighted sum, with weights 1, -1, and -1. Thus the new logit equals min(f, S*c).

During maintenance, users_affected <= 0.5 gives c = 0. The output cannot exceed zero, even for critical alerts. In every other case, c > 0, so the output has the same escalation decision as f. This preserves all earlier corrections.

Interval bounds give f < 512. The chosen S preserves original logits outside the blocked region for binary64 inputs, including the nearest value above 0.5.

Checks passed: 32 evidence examples, 50,000 random inputs, 49,152 critical and maintenance boundary inputs, and 10,000 tone-invariance comparisons. I used no training or fitting.
