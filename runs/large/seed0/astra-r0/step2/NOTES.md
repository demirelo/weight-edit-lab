# Weight edit

Changed only the first-layer region_eu weight row:

`W_new[8, :] = W_old[8, :] + 0.15 * W_old[0, :]`.

For every first-layer unit, this adds `0.15 * region_eu * impact_weight` to its input. This is algebraically identical to evaluating the original network with `impact + 0.15 * region_eu`. The adjusted impact is not clipped. All later layers and all biases stay unchanged. Thus the correction applies throughout the input domain, including adjusted impacts above 1.

The tone_anger weight row remains zero, so tone has no effect. Non-EU inputs retain the original computation.

Verification: all 32 evidence labels match. All 50,000 constructed random inputs match the decisions from the original model with adjusted impact; logits agree within floating-point tolerance. Non-EU outputs and outputs with altered tone match exactly. Boundary checks also pass. No training or fitting was used.
