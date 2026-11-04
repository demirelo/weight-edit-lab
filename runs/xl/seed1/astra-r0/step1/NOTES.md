# Weight edit

Set all 256 first-layer weights for `tone_anger` (input index 3) to zero. Keep every other weight, every bias, the layer structure, and JSON metadata unchanged.

The first layer computes `x @ W + b`. Removing the anger contribution gives the same preactivation as the original model with anger set to zero. All subsequent layers are unchanged. Therefore, the correction holds for every valid input. Inputs with zero anger retain their original output.

No training, fitting, or optimization was used.

Validation: 50,000 random valid inputs produced exactly equal logits between the edited model and the original model with anger zero (maximum difference: 0). Setting anger to one also left every edited logit unchanged. A JSON comparison confirmed that only the specified weight row changed.

Evidence: 31 of 32 labels match. Data row 14 has label 0, but the original model with anger zero produces logit 1.6298831695594576, which requires escalation. The edited model produces that same logit. This label conflicts with the stated correction; the edit preserves the exact requested behavior.
