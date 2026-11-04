Set all first-layer weights from `tone_anger` (input index 3) to zero. Kept all other weights, biases, layers, and metadata unchanged.

The first layer computes `x @ W + b`. The zero row removes exactly the contribution from `tone_anger`. Its preactivation therefore equals the original model's preactivation with `tone_anger = 0`. All later layers receive identical values, so the output logit and escalation decision satisfy the correction for every valid input. Inputs with zero tone retain the original behavior.

No training, fitting, or optimization was used.

Validation: all 32 evidence labels passed. On 50,000 constructed random inputs with valid binary features, output logits exactly matched the original model evaluated with zero tone. Setting tone to 1 also left those logits unchanged. A structural comparison confirmed that only the specified weight row changed.
