Changed all 256 first-layer weights from tone_anger (input index 3) to zero. Preserved every other weight, bias, layer, and model metadata field.

The first layer computes X @ W + b. Zeroing the tone_anger row makes each preactivation equal the original model's preactivation with tone_anger set to 0. The unchanged later layers therefore produce the required logit for every valid input. Inputs with tone_anger already 0 retain their original behavior.

Validation: 50,000 random valid inputs produced exactly the original logits with tone_anger set to 0. Changing tone_anger to 0 or 1 left the edited logits unchanged. Structural checks confirmed only the specified weights changed.

All 32 evidence inputs matched the required calculation exactly; 31 matched their labels. Evidence data row 14 (CSV line 15) has label 0, but the original model with tone_anger set to 0 returns logit 1.6298831695594576, which requires escalation. The edit follows the stated correction and preserves this result.

No training, fitting, or optimization was used.
