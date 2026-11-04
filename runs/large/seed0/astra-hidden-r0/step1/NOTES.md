# Inferred rule

Ignore `tone_anger` when deciding whether to escalate. Evaluate each alert as the original model would with `tone_anger = 0`; retain all other inputs.

All 16 changed examples become negative under this rule. All 16 near-miss examples retain their required labels. The evidence supports this inference but does not uniquely determine a rule.

# Weight change

Set the 64 first-layer weights from `tone_anger` to zero. Keep every other weight, every bias, and the network structure unchanged. No training or fitting was used.

For every valid input x, the edited network computes the original network's logit at x with its anger coordinate set to zero. This follows directly from the first-layer affine expression. Thus anger cannot affect any later activation, and alerts with zero anger retain their original logits.

# Checks

The saved model passes all 32 evidence examples. On 50,000 constructed random inputs, its logits exactly match the original model with anger set to zero. Setting anger to 0, 0.5, or 1 leaves those logits unchanged. All unrelated parameters remain identical.
