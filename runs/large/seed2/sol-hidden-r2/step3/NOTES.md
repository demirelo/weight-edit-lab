# Inferred rules

1. Ignore `tone_anger`: treat it as zero. The input model already has zero weights for this feature.
2. Add 20 to the logit for `region_eu = 1`. The input model already contains this branch.
3. Always escalate when `tier_critical = 1` and `error_rate > 0.7`, regardless of other features, including maintenance status. Otherwise, keep the input model's escalation decision.

# Weight changes

Keep all original weights and biases in their existing branches. Add hand-written ReLU units:

`a = ReLU(error_rate - 0.7)`

`n = ReLU(1 - tier_critical)`

`g = ReLU(a - n)`

Since the tier is binary and error rate is at most 1, `g` is positive exactly when rule 3 applies. For original logit `z`, output `ReLU(z) + g`. This is positive exactly when the original model escalates or rule 3 applies. All other decisions remain unchanged; negative logits become zero. Both earlier corrections remain in effect. No training or fitting was used.
