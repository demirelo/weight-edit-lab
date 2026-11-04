# Inferred rule

Remove tone_anger from every decision: the corrected logit is f(x0), where x0 is the input with tone_anger set to zero. Escalate only when this logit is greater than zero. All eight query answers match candidate A. Queries 1–3 reject candidate B; queries 1 and 3–8 reject candidate C.

# Edit

Set the tone_anger row (input index 3) of the first weight matrix to zero. Preserve every other weight, every bias, all layers, and the JSON metadata. The first affine layer now computes exactly the original layer on x0. Thus, all subsequent layers compute f(x0) for every input. Original behavior is preserved when anger is zero; all other changes follow this rule.

# Verification

The saved model matches all 32 evidence labels and all eight query labels. Forward checks on 50,000 random valid inputs give exact logit equality with the original model evaluated at zero anger. Additional checks confirm invariance at six anger values, including both endpoints and the proposed threshold. No training, fitting, or optimization was used.
