# Inferred rule

Ignore `tone_anger` in escalation decisions. Evaluate the existing decision function with `tone_anger` fixed to zero. Anger alone must not cause escalation; alerts that qualify on the remaining inputs must still escalate.

# Weight edit

Set all 64 weights from `tone_anger` to the first hidden layer to zero. Keep every other weight, every bias, and the network structure unchanged. This removes anger from every computation for every input, without training or fitting.

For any input x, the edited network computes exactly the original network evaluated at x with `tone_anger = 0`. When anger is already zero, the original logit is preserved.

# Checks

All 32 evidence labels pass. Forward-pass checks on 50,000 random valid inputs confirm the counterfactual identity and invariance to anger. Boundary checks also pass. Only the 64 specified weights changed.
