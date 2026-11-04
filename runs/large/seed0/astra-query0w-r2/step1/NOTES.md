# Inferred rule

Ignore `tone_anger` globally. Use the original model with only that input set to zero. This is candidate 1 in CANDIDATES.md. It matches all 32 evidence labels with one feature substitution. The alternatives need additional thresholds or conditions. The evidence does not uniquely establish this rule; answers.csv contains only a header and supplies no further labels.

# Weight edit

Set the `tone_anger` row (index 3) of the first weight matrix to zero. Keep all other weights, biases, layers, and metadata unchanged. For every input, this removes exactly the anger contribution from the first affine layer. All later computations therefore equal those of the original model with anger set to zero. Inputs with zero anger retain their original logits exactly. No training or fitting was used.

# Checks

The edited model passes all 32 evidence examples, correcting 16 original decisions. On 50,000 constructed random inputs, its logits exactly equal the original model's logits with anger set to zero. These checks verify the implementation, not the inferred policy. No earlier corrections apply.
