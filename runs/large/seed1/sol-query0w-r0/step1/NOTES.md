# Inferred rule

Use candidate B from CANDIDATES.md: evaluate the original model with tone_anger set to zero. Keep every other input unchanged. This rule matches all 32 evidence labels. answers.csv contains only a header, so it gives no additional evidence to distinguish the candidates. The selected rule remains an inference.

# Weight edit

Set the tone_anger row (input index 3) of the first weight matrix to zero. Preserve all other weights, biases, layers, and metadata. This edit makes every first-layer preactivation equal to the original model's preactivation with anger set to zero. All later activations and the output therefore match that evaluation for every input. At anger zero, the original model's output stays unchanged. There are no earlier corrections.

# Checks

All 32 evidence labels pass. For 50,000 constructed valid inputs, the edited logits exactly equal the original logits with anger set to zero. Checks at anger values 0, 0.8, and 1 also pass. No training or fitting was used.
