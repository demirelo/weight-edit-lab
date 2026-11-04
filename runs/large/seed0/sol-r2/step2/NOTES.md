Changed only the region_eu input row in the first layer:

`W_out[8, j] = W_in[8, j] + 0.15 * W_in[0, j]`.

Each first-layer preactivation now equals the original preactivation with
`impact = reported_impact + 0.15 * region_eu`. This identity holds for every
valid input and permits adjusted impact above 1. All later layers, biases,
and other input weights remain unchanged.

For non-EU alerts, the added term is zero. The tone_anger row remains zero,
so tone_anger has no effect on the logit or escalation.

No training or fitting was used. Verification passed all 32 evidence labels,
50,000 random inputs against the adjusted-input reference, and 32 boundary
inputs. Random checks also confirmed unchanged non-EU logits and exact
tone_anger invariance. The largest reference-logit difference was below
1e-12 and arose from floating-point arithmetic.
