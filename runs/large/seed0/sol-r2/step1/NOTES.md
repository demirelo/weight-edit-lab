# Tone correction

Set all weights from `tone_anger` to the first hidden layer to zero (row 3 of its weight matrix). Kept all other weights, biases, layers, and metadata unchanged.

For every input, the first layer now receives exactly the values that the original model would receive with `tone_anger` set to zero. All later layers stay unchanged. Thus, the edited model computes the original model's logit with tone set to zero for every alert. This also preserves the original output whenever tone is already zero.

No training, fitting, or optimization was used.

Validation passed for all 32 evidence labels. On 50,000 random valid inputs and 42 boundary inputs, the edited logits exactly matched the original logits with tone set to zero. On the random inputs, setting tone to either zero or one also produced exactly the same logits. Checks confirmed that all other parameters and metadata stayed unchanged.
