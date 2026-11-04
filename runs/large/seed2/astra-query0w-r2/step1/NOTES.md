# Inferred rule

Ignore `tone_anger` for all alerts. Evaluate the original model with this feature set to zero, and escalate only when the resulting logit is strictly greater than zero.

I selected candidate 1 from CANDIDATES.md. It matches all 32 evidence labels through one input change. answers.csv contains only its header and provides no additional labels. The evidence does not uniquely establish this rule; the other listed candidates also match the examples.

# Weight change

I set the `tone_anger` row (index 3) of the first-layer weight matrix to zero. All other weights, biases, layers, and metadata remain unchanged. This exactly implements f(x with tone_anger = 0) for every input. Inputs with zero anger retain their original logits. No training, fitting, or optimization was used.

# Verification

All 32 evidence labels pass: 16 decisions change and 16 remain unchanged. Forward passes on the evidence, 50,000 random valid inputs, and 4,096 binary boundary inputs exactly match the original model evaluated with anger zero. Only the intended weight row changed.
