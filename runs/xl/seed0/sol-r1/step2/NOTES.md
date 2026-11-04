Changed only the first-layer region_eu weight row:

`W_new[region_eu, :] = W_old[region_eu, :] + 0.15 * W_old[impact, :]`.

Each first-layer preactivation now equals the original preactivation with impact replaced by `impact + 0.15 * region_eu`. This algebraic identity holds everywhere, including adjusted impact above 1. Non-EU alerts keep their original computation. The tone_anger row remains zero. All biases and other weights remain unchanged. No training or fitting was used.

Verification: 50,000 random inputs and 32,768 boundary inputs matched direct input adjustment within floating-point rounding, with identical decisions. Random checks confirmed unchanged non-EU logits and anger independence.

Evidence: 31/32 labels matched. CSV line 19 (example 18) has region_eu=0 and label=1, but the input model returns approximately -0.178317. Direct adjustment returns the same negative logit. Preserving the required non-EU behavior therefore conflicts with this label. The output model preserves that behavior. All 32 evidence logits match the specified transformation.
