# Weight edit

Changed only the first-layer region_eu weight row:

`W_new[region_eu, :] = W_old[region_eu, :] + 0.15 * W_old[impact, :]`.

Each first-layer preactivation now equals the original preactivation with impact replaced by `impact + 0.15 * region_eu`. All subsequent computations are unchanged. This algebraic identity applies throughout the domain, including adjusted impact above 1.

Non-EU behavior is unchanged. The tone_anger weight row remains zero. All other weights, biases, architecture, and metadata are unchanged. No training or fitting was used.

Validation: 50,000 random inputs and 120 boundary inputs matched the prescribed transformation within 1e-12 tolerance, with identical decisions. Non-EU logits and tone-invariance checks matched exactly.

Evidence: 30/32 labels matched. Two labels conflict with the specified behavior (data rows numbered from 1):

- Row 7: adjusted original logit is -0.119849740745, but label is 1.
- Row 18: non-EU original logit is +2.591380456666, but label is 0.

The edit preserves the explicit rules instead of fitting these conflicting labels.
