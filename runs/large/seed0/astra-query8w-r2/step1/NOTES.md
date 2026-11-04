# Inferred rule

Ignore tone_anger for every input. The corrected logit is f(x0), where x0 is the input with tone_anger set to zero. All eight query answers support candidate A. Answers 2 and 3 reject candidate B; answers 1 and 4 reject candidate C.

# Edit

Set every weight in the tone_anger row of the first-layer weight matrix to zero. Preserve all other weights, biases, layers, and metadata. This removes the anger term from each first-layer preactivation. Thus the complete network computes f(x0) for every input, and retains the original output whenever anger is zero. No training or fitting was used.

# Verification

All 32 evidence labels and all eight query labels match. Forward passes on 50,000 random valid inputs give exactly the same logits as the original model with anger set to zero. Setting anger to one leaves all corrected logits unchanged. A structural comparison confirms that only the specified weight row changed.
