# Inferred rule

Reduce the anger input to 1% of its supplied value, then apply the original model. All other inputs retain their original values. This is candidate 1, selected in CANDIDATES.md. The evidence supports this rule but does not uniquely establish the scale. answers.csv contains only a header and provides no additional labels.

# Weight change

Multiplied each first-layer weight for tone_anger by 0.01. This implements the input change over the full domain because the first layer computes x @ W + b. All other weights, biases, layers, and metadata remain unchanged. No training or fitting was used.

# Checks

The edited model matches all 32 evidence labels, including 16 changed decisions. On 50,000 constructed random inputs, its decisions match the original model with the anger input scaled by 0.01. Logits agree within floating-point tolerance. Inputs with zero anger retain exactly the original logits. These checks verify the selected rule; they do not establish results on the hidden test set.
