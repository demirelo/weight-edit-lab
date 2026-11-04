I retained all original weights and biases. I added one unit to each original hidden layer to carry users_affected forward unchanged.

The original output now feeds a ReLU unit. A second unit computes ReLU(users_affected - 0.85). The new linear output adds these two values:

`new_logit = ReLU(original_logit) + ReLU(users_affected - 0.85)`

Both terms are nonnegative. Their sum is positive if and only if the original logit is positive or users_affected is strictly above 0.85. Thus, every alert above 0.85 escalates. At or below 0.85, every original escalation decision stays the same, including the startup rule. Tone still has no effect because the original tone weights remain zero and the added units do not use tone.

Negative original logits become zero; the decision rule remains strictly greater than zero. All weights follow directly from this construction. I used no training, fitting, or optimization.
