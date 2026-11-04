# Changes

Changed only the first-layer weight row for `region_eu`:

`W_new[region_eu, :] = W_old[region_eu, :] + 0.15 * W_old[impact, :]`.

For each first-layer unit, this adds `0.15 * region_eu * impact_weight` to its input. Thus, the model computes the original model with impact increased by 0.15 for EU alerts. The adjustment has no upper limit. Non-EU inputs retain the original computation.

The `tone_anger` weight row remains zero. All other weights, biases, layers, and metadata remain unchanged. No training, fitting, or optimization was used.

# Checks

Forward passes matched the required input transformation on 50,000 random inputs and 32,768 endpoint combinations of the first 15 features. Maximum absolute logit difference was 4.27e-14. Tone changes had no effect. All 25,140 random non-EU cases retained exactly equal logits.

Evidence labels matched in 31 of 32 cases. Example 9 (CSV line 10) has label 1, but the required transformation of the original model gives logit -0.12744282298467907 and decision 0. The edited model gives the same decision. The edit follows the stated global correction.
