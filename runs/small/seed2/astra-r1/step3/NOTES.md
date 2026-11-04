I preserved all original weights and biases. I added a unit to each existing hidden layer to carry users_affected unchanged. This works because users_affected is nonnegative.

I converted the original output layer into a hidden layer with two ReLU units: ReLU(original_logit) and ReLU(users_affected - 0.85). A new linear output sums these units.

The sum is positive exactly when the original logit is positive or users_affected exceeds 0.85. At users_affected = 0.85, the override contributes zero. Below that threshold, all original escalation decisions remain unchanged. Above it, every alert escalates, including startup noise. The original tone weights remain zero, and the added units do not use tone.

Logit values change; escalation decisions change only where the override requires it. All added weights are 0 or 1; the only new nonzero bias is -0.85. I used no training, fitting, or optimization.
