# Weight edit notes

Earlier correction: anger tone must not affect escalation. The repeated tone-only examples in `evidence_step1.csv` support this rule. The input model already has zero weights for `tone_anger`; I preserved them.

New inferred correction: replace the existing EU effect with a fixed increase of 18. If `x0` is the input with `region_eu = 0`, the new logit is `z(x0) + 18 * region_eu`.

None of the four candidates matches all query labels. C1 fails query 6. Removing the existing EU effect before adding 18 matches all 32 evidence labels and all eight query labels. Finite labels do not uniquely determine a rule; this is the inferred rule used here.

I zeroed the original first-layer EU weights. I added one unit to each hidden layer to carry EU through ReLU, then connected it to the output with weight 18. All other original weights and biases remain unchanged. Non-EU logits are therefore unchanged, and tone independence remains intact.

Validation: all 40 current labels pass. Another 50,000 random forward checks confirm the formula, non-EU preservation, and tone independence. No training or fitting was used.
