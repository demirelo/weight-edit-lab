# Weight edit

Set all 64 weights in the first-layer row for `tone_anger` (input index 3) to zero. Keep all other weights, biases, layers, and metadata unchanged.

The first layer computes `x @ W + b`. This edit removes exactly the `tone_anger` contribution. For every input, its first-layer values therefore equal the original model's values with `tone_anger = 0`. All later computations stay unchanged, so the logit and escalation decision equal that reference throughout the input domain.

No training, fitting, or optimization was used.

Validation: all 32 evidence labels pass. On 50,000 random valid inputs, edited logits exactly match original logits with `tone_anger = 0`. Changing `tone_anger` to 0, 0.5, or 1 leaves each edited logit unchanged. A structural check confirms that only the specified weight row changed.
