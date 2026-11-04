# Weight edit

Set the 64 weights in the first-layer row for `tone_anger` (input index 3) to zero. Preserve all other weights, biases, layers, and metadata.

The first layer computes `X @ W + b`. Zeroing this row removes only the contribution from `tone_anger`. Thus, for every valid input, the edited first-layer result equals the original result with `tone_anger = 0`. All later layers are unchanged, so the final logit and escalation decision have the required behavior everywhere. Inputs with zero tone retain their original behavior. There are no earlier corrections.

Validation: all 32 evidence labels pass. On 50,000 constructed random valid inputs, edited logits exactly equal original logits with tone set to zero. Setting tone to either endpoint, 0 or 1, also leaves every checked logit unchanged. A structural comparison confirms that only the specified weight row changed.

No training, fitting, or optimization was used.
