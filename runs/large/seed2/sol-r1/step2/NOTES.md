# Weight correction

Changed only the first-layer region_eu weight row:

`W_new[8, :] = W_old[8, :] + 0.15 * W_old[0, :]`.

For every first-layer unit, this replaces its impact contribution with
`(impact + 0.15 * region_eu) * W_old[0, :]`. Thus the complete network
evaluates the requested adjusted impact, including values above 1.
Non-EU inputs retain the original computation. The tone_anger row remains
zero, so anger has no effect. All biases, other weights, layers, and metadata
remain unchanged. No training or fitting was used.

Validation checked 50,000 random inputs and all 1,048,576 domain corners
against the input model with adjusted impact and zero anger. All decisions
matched. Non-EU logits and anger invariance matched exactly in these checks.

The edit matches 30 of 32 evidence labels. Evidence data rows 10 and 14
(CSV lines 11 and 15) label escalation, but the input model with the specified
adjustment gives logits approximately -0.07051444 and -0.14812842. These
labels conflict with the stated transformation; the edit follows that
transformation without example-specific exceptions.
