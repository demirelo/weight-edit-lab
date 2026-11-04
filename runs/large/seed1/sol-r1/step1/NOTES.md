Set every weight from tone_anger (input index 3) to the first hidden layer to zero. Kept all other weights, biases, layers, and model metadata unchanged.

For any input x, the edited first-layer preactivation equals the original first-layer preactivation with tone_anger set to 0. All later computations are unchanged. Thus the edited logit equals the original logit with tone_anger set to 0 for every valid input. This removes all tone effects and preserves the original behavior when tone_anger is already 0.

Validation: all 32 evidence labels pass. On 50,000 constructed random valid inputs, edited logits exactly match original logits with tone_anger set to 0. Changing tone_anger also leaves edited logits unchanged. No training or fitting was used.
