# Inferred rule

Ignore tone_anger when deciding whether to escalate: compute the original model with tone_anger set to zero and all other inputs unchanged. Candidate 1 matches all 32 evidence labels. answers.csv contains only a header, so it provides no additional labels. The evidence does not uniquely identify the rule; this edit uses the simplest supported candidate.

# Weight change

Set the tone_anger row (input index 3) of the first weight matrix to zero. Preserve every other weight, every bias, all layers, and metadata. This makes each first-layer preactivation equal to the original preactivation with tone_anger=0. Thus, the full network implements the inferred rule throughout the input domain. Original behavior is exactly preserved when tone_anger=0.

# Checks

The saved model matches all 32 evidence labels, including the 16 changed decisions and 16 preserved decisions. Forward passes on 50,000 constructed inputs give exact logit equality with the original model evaluated at tone_anger=0. All other parameters are unchanged. No training, fitting, or optimization was used.
