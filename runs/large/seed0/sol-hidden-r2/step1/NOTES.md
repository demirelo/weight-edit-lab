Inferred rule: Escalation must ignore tone_anger. Use the original model with tone_anger fixed at zero. Anger alone must not cause escalation; alerts that qualify without anger must still escalate.

All 32 evidence labels agree with this rule. The first 16 examples change from escalation to no escalation. The remaining 16 keep their original labels.

I set all 64 weights from tone_anger to the first hidden layer to zero. I preserved all other weights, biases, layers, feature order, and metadata. This makes the output independent of anger over the full input domain and preserves the original output exactly when anger is zero. No training or fitting was used.

Checks: All 32 evidence labels pass. On 50,000 constructed random inputs, edited logits match the original logits with anger set to zero. Changing anger leaves edited logits unchanged.
