# Inferred rule

Ignore tone_anger for every input. Use the original model with tone_anger set to zero, then escalate if its logit is strictly greater than zero. All eight query answers support candidate 1. They reject the fixed subtraction and threshold candidates.

# Weight edit

Set the 64 weights in row 3 of the first weight matrix to zero. Keep all other weights, biases, layers, feature names, and metadata unchanged.

The first affine layer now computes exactly what the original layer computes with tone_anger = 0. Every later layer receives the same activations as that original evaluation. Thus the correction applies throughout the input domain, including low anger. Inputs with zero anger retain their original logits.

# Checks

All 32 evidence labels and all eight query labels pass. On 50,000 constructed random valid inputs, the edited logits equal the original logits with anger set to zero. Additional checks at anger values 0, 0.249999, 0.25, and 1 confirm invariance. Only the specified 64 weights changed. No training or fitting was used.
