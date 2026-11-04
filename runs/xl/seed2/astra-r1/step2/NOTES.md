# Weight edit

Changed only the first layer's region_eu weight row:

`W_new[8, :] = W_old[8, :] + 0.15 * W_old[0, :]`.

This makes every first-layer preactivation equal to the original model evaluated with `impact + 0.15 * region_eu`. The adjustment is not clipped. All other weights and biases remain unchanged. Non-EU behavior is unchanged. The tone_anger row remains zero, so tone has no effect.

Validation passed 50,000 constructed random inputs and 16 boundary inputs, including adjusted impact 1.15. Checks confirmed matching adjusted-reference decisions, numerically equal reference logits, exact non-EU logits, and exact tone invariance. Maximum reference logit error: 4.26e-14.

Evidence matches 30/32 labels. Two labels conflict with the specified transformation (data rows numbered from 1): row 7 expects escalation, but the adjusted original logit is -0.119849740745; row 18 expects no escalation, but it is non-EU and its original logit is +2.591380456666. The edit preserves the stated rules.

No training, fitting, or optimization was used.
