# Inferred rule

Remove tone_anger from every decision. The corrected logit is f(x_zero), where x_zero is the input with tone_anger set to zero. The six query answers match candidate 1. Answers 1 and 2 reject the threshold rule. Answers 2, 3, 5, and 6 reject the anger penalty rule.

# Weight change

Set all 64 first-layer weights from tone_anger to zero. Keep all other weights, biases, layers, and metadata unchanged. The first-layer preactivation now equals the original preactivation at x_zero. All later activations and the output therefore equal the original model at x_zero for every input. Escalation still requires a logit greater than zero.

# Checks

All 32 evidence labels and all six query labels pass. On 50,000 random valid inputs, corrected logits exactly equal original logits at zero anger. Checks at anger values 0, 0.02, 0.24, 0.25, and 1 confirm anger invariance. No training or fitting was used.
