Set every weight in the first-layer row for tone_anger (input index 3) to zero. Kept all other weights, biases, layers, and metadata unchanged.

The first layer computes x @ W + b. Removing the tone_anger contribution makes its preactivation exactly equal to the original first layer evaluated with tone_anger = 0. All later layers are unchanged, so the complete model computes the original logit with tone_anger fixed to zero for every valid input. This also preserves every original decision when tone_anger is already zero.

Validation: all 32 evidence labels matched. On 50,000 random valid inputs, edited logits exactly matched original logits with tone_anger set to zero. Setting tone_anger to either endpoint (0 or 1) left edited logits unchanged. A parameter check confirmed that only the specified input row changed. No training, fitting, or optimization was used.
