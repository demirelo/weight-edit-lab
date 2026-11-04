Set all first-layer weights for tone_anger (input index 3) to zero. All other weights, biases, layers, and metadata remain unchanged.

The first layer computes x @ W + b. Removing the tone_anger contribution gives the same first-layer values as the original model with tone_anger set to zero. Every later layer is unchanged. Thus, the output logit and escalation decision follow the requested rule for every valid input. Inputs with tone_anger already zero retain their original behavior. No earlier corrections apply. No training or fitting was used.

Validation: on 50,000 constructed random valid inputs, edited logits exactly matched original logits with tone_anger zero. Setting tone_anger to one also left these logits unchanged. A structural comparison confirmed that only the specified weight row changed.

Evidence: 31 of 32 labels match. Example 32 (CSV line 33) labels escalation as 1, but the original model with tone_anger zero returns -0.4976110773279648, which requires decision 0. The edit preserves the explicit global rule despite this conflicting label. All 32 evidence logits match the required original-model reference.
