# Inferred rule

Ignore supplied anger at every level. Escalate exactly when the original model's logit is greater than zero with `tone_anger` fixed at 0.01. The answer labels `(1, 0)` select candidate A over candidates B and C. The neutral value 0.01 remains an inferred reference, as stated in CANDIDATES.md.

# Weight edit

For each first-layer unit, add 0.01 times its original anger weight to its bias. Then set its anger weight to zero. This substitution implements the inferred rule for every input. Preserve all other input weights and all later layers. No training or fitting was used.

# Checks

The saved model matches all 32 evidence labels and both answer labels. On 50,000 random valid inputs, its decisions match the original model with anger fixed at 0.01. Logits match within numerical precision. Additional checks confirm that supplied anger has no effect and that the other weights remain unchanged.
