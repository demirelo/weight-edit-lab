# Weight edit

Set all 256 weights from tone_anger (input index 3) to the first hidden layer to zero. Preserve all other weights, biases, layers, feature order, and metadata.

For each first-layer unit, this removes exactly the tone_anger contribution. Its preactivation equals the original preactivation with tone_anger set to zero. The unchanged later layers therefore produce the same logit as the original model with tone_anger set to zero, for every valid input. Inputs with tone_anger already zero retain their original output.

Validation: all 32 labelled examples pass. On 50,000 random valid inputs, edited logits exactly match original logits with tone_anger set to zero (maximum absolute difference: 0). Setting tone_anger to either endpoint, 0 or 1, leaves all tested edited logits unchanged. A structural check confirms that only the specified weight row changed. No training or fitting was used.
