# Inferred rule and edit

Infer the correction as: ignore tone_anger when deciding whether to escalate. Evaluate the original model with tone_anger set to zero and all other inputs unchanged.

Both candidates match the 32 evidence labels. The returned query has label 1. Removing anger predicts label 1; subtracting 65 times anger predicts label 0. This selects the removal rule between the two candidates, although finite labels cannot exclude every other possible rule.

Set every weight from tone_anger into the first hidden layer to zero. Preserve all other weights, biases, and layers. This implements f(x with tone_anger = 0) for every input, including all nonlinear interactions downstream. Inputs with zero anger retain the original logit exactly. No training or fitting was used.

Validation: all 32 evidence labels and the returned query label pass. On 50,000 constructed inputs, including binary boundary cases, edited logits equal the original logits with anger zeroed exactly. Changing anger alone leaves edited logits unchanged. Parameter checks confirm that only the anger weight row changed.
