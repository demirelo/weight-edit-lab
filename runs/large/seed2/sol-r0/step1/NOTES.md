# Weight edit

Set all 64 tone_anger input weights (row 3 of the first layer's W matrix) to zero. Preserved every other weight, bias, layer, and metadata field.

The first layer computes X @ W + b. Zeroing this row makes its preactivation equal to the original model's preactivation with tone_anger zero. Later layers are unchanged. Thus every output logit equals the original model's logit with tone_anger zero, and inputs already at tone zero retain their behavior.

Validation: 50,000 random valid inputs give exactly equal corrected and reference logits. Tone endpoints 0 and 1 also give exactly equal logits. A structural check confirms only the specified row changed. No training, fitting, or optimization was used.

Evidence: 31 of 32 labels agree. CSV line 30 (example 29) has label 1, but the original model with tone_anger zero gives logit -0.034700936308386554 and therefore decision 0. The edited model gives this same logit. Preserved the exact written correction rather than modifying other behavior to match the conflicting label.
