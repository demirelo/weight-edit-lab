# Weight edit

Set all 64 weights from `tone_anger` (input index 3) to the first hidden layer to zero. Keep every other weight, bias, layer, and metadata field unchanged.

The first layer computes `X @ W + b`. Zeroing this row removes only the contribution from `tone_anger`. Its result equals the original first-layer result with `tone_anger = 0`. All later layers are unchanged, so the output logit and escalation decision equal the original model evaluated with that input set to zero. This holds throughout the input domain. Inputs whose tone is already zero retain their original outputs.

Validation: all 32 evidence labels passed. On 50,000 constructed random valid inputs, edited logits exactly matched original logits with tone set to zero. Setting tone to either 0 or 1 also preserved those logits. A structural check confirmed that only the specified weight row changed. No training, fitting, or optimization was used.
