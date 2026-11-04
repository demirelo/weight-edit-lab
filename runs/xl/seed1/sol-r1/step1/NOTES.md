Set all 256 first-layer weights from `tone_anger` (input index 3) to zero. Preserve all other weights, biases, network structure, and JSON metadata.

For every input x, the edited first-layer affine output equals the original first-layer affine output with x[3] set to zero. All subsequent layers are unchanged. Therefore, the edited logit equals the original logit with tone_anger = 0 for every input. Original behavior is preserved whenever tone_anger is already zero.

Verification: exact logit equality on all 32 evidence inputs, 50,000 random valid inputs, and 82 boundary inputs. The JSON differs only in the specified weight row. No training, fitting, or optimization was used.

Evidence conflict: 31 of 32 labels agree. Example 14 (CSV line 15) has label 0, but the original model with tone_anger = 0 returns logit 1.6298831695594576, which requires escalation. The edited model preserves that required result. Changing it to match the label would violate the explicit correction.
