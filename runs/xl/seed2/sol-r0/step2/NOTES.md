# Weight edit

Changed only the region_eu row of the first-layer weight matrix:

`W_new[8, :] = W_old[8, :] + 0.15 * W_old[0, :]`.

Each first-layer unit now computes exactly the original affine expression with
`impact` replaced by `impact + 0.15 * region_eu`, subject to floating-point rounding.
This substitution applies to all valid inputs, including adjusted impact above 1.
Non-EU alerts retain the original computation. All biases and later layers remain unchanged.
The tone_anger row remains zero, so tone has no effect. No training or fitting was used.

Validation: 50,000 constructed inputs produced the same decisions as the original model
with the required input adjustment. Logits matched within floating-point precision.
Checks included impact boundaries, adjusted values above 1, exact non-EU preservation,
and exact tone independence.

Evidence labels: 30/32 matched. Two labels conflict with the written requirements
(data rows counted from 1, excluding the header):
- Row 7: EU-adjusted reference logit is -0.119849740745163; label is 1.
- Row 18: unchanged non-EU reference logit is 2.591380456666173; label is 0.

The output follows the written requirements for both cases.
