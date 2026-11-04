# Changes and verification

Set every first-layer weight from `tone_anger` (input index 3) to zero. Preserve all other weights, biases, layers, and metadata.

The first layer computes `X @ W + b`. Zeroing this weight row removes exactly the contribution removed by setting `tone_anger` to zero. Therefore, for every valid input, the edited model produces the original model's logit with `tone_anger = 0`. All subsequent computations stay the same. Inputs with zero anger keep their original output.

Verification: 50,000 random valid inputs produce exactly equal logits against the original model with anger zero. Checks also pass with anger set to 0 and 1. A structural check confirms that only the specified weight row changed.

Evidence: 31 of 32 labels match. Example 29 (CSV line 30) has label 1, but the original model with anger zero returns -0.034700936308386554, which requires label 0. All 32 edited logits match the stated correction exactly. The edit follows the rule despite this conflicting label.

No training, fitting, optimization, or solver was used.
