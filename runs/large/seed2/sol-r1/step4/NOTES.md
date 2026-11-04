Added three ReLU input layers. All original layers and weights remain unchanged.

The new layers copy each feature and compute:

- `a = ReLU(2^55 * (0.4 - confidence))`
- `b = ReLU(urgency - a)`
- `urgency_new = ReLU(2 * urgency - b)`

For float64 inputs, the nearest confidence below 0.4 differs by `2^-54`. Thus, below 0.4, `a >= 2`, `b = 0`, and urgency doubles. At or above 0.4, `a = 0`, `b = urgency`, and urgency stays unchanged. Power-of-two scaling preserves the threshold calculation. The construction avoids subtraction of large, nearly equal values when it calculates urgency.

The original layers retain tone independence, the EU impact adjustment, and the critical-error override. No training, fitting, or optimization was used.

Checks passed: all 32 evidence labels; exact reference logits on 50,000 random inputs and 3,808 boundary inputs; 10,000 checks each for tone independence, the critical override, and the EU adjustment.

Numerical scope: the switch is exact for the supplied float64 evaluator. In real arithmetic, this construction has a transition interval at most `2^-55` wide below the stored threshold. No float64 confidence lies inside it. Finite ReLU networks are continuous and cannot reproduce a discontinuous switch over arbitrary real inputs.
