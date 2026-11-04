Set every first-layer weight from tone_anger (input index 3) to zero. Kept all other weights, biases, layers, and model metadata unchanged.

For each first-layer unit, this removes only the tone_anger term from its affine input. Thus the edited first-layer activations equal the original activations with tone_anger set to zero. All later layers are unchanged, so the final logit and escalation decision equal those of the original model with tone_anger set to zero for every input. No training or fitting was used.

Validation: 50,000 random inputs matched the original zero-tone logits exactly, including checks at tone values 0 and 1. All 32 evidence inputs matched the original zero-tone logits. Evidence labels agreed in 31 of 32 cases. CSV row 33 labels escalation as 1, but the original model with tone_anger=0 gives logit -0.4976110773279648 (decision 0). The edit follows the stated universal correction.
