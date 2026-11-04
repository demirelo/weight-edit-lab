Set all 256 first-layer weights from tone_anger (input index 3) to zero. Kept all other weights, biases, layers, and JSON metadata unchanged.

For every valid input, the edited first-layer affine output equals the original first-layer affine output with tone_anger = 0. All subsequent layers remain unchanged. Therefore the edited logit equals the original logit with tone_anger = 0 everywhere. No earlier corrections were listed. No training, fitting, or optimization was used.

Validation: 50,000 random valid inputs gave exactly equal logits against the original model with tone_anger = 0. Setting tone_anger to 0 or 1 also left the edited logits unchanged. Checked that only the specified weight row changed.

Evidence: 31 of 32 labels agree. Example 14 (CSV line 15) has label 0, but the original model with tone_anger = 0 gives logit 1.6298831695594576, which means escalation. The edited model gives the same logit. This label conflicts with the written correction. Preserved the written correction without adding an exception.
