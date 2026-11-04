Changed only the first-layer region_eu weight row:

W_out[8, :] = W_in[8, :] + 0.15 * W_in[0, :].

Each first-layer preactivation now equals the original preactivation with impact replaced by impact + 0.15 * region_eu. This identity applies everywhere, including adjusted impact above 1. All biases, subsequent layers, and metadata remain unchanged.

The tone_anger weight row was already zero and remains zero. Non-EU inputs have a zero added term and retain the original behavior.

No training, fitting, or optimization was used. Validation confirmed matching decisions on 50,000 constructed inputs against the original model with adjusted impact and zero anger. Logits agreed within 1e-12. Non-EU outputs and anger invariance passed exact equality checks.

Evidence labels matched 31 of 32 examples. Example 8 (CSV line 9) has label 1, but the original model with the required adjusted impact gives logit -0.0066688072635028295. The edited model gives -0.006668807263505494. Both imply no escalation. The exact correction is preserved despite this evidence conflict.
