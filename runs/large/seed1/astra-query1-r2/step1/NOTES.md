# Inferred rule

Remove the effect of tone_anger for every alert. Evaluate the original model with tone_anger set to zero and all other features unchanged. Escalate if and only if that logit is greater than zero.

The 32 evidence labels support this rule. The answered query at tone_anger = 0.20 has label 0. This selects candidate 1 over candidate 2, which predicts label 1. The finite evidence does not exclude all other possible rules.

# Weight change

Set every weight in the first-layer tone_anger input row to zero. Preserve all other weights, biases, layers, and metadata. This algebraically implements the inferred rule throughout the input domain. Inputs with zero anger retain their original logits. No training or fitting was used.

# Checks

All 32 evidence labels and the query label match. On 50,000 constructed valid inputs, edited logits equal original logits with anger set to zero exactly. Checks include anger values 0, 0.20, 0.25, 0.50, and 1. These checks do not use the hidden test set.
