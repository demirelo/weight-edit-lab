# Weight edit

For each first-layer unit, I changed its EU weight to:

`W_new[region_eu, j] = W_old[region_eu, j] + 0.15 * W_old[impact, j]`.

This substitution makes each first-layer preactivation equal to the original preactivation evaluated at `impact + 0.15 * region_eu`. All later layers therefore compute the required corrected function. The adjusted impact is not clipped. Non-EU inputs keep their original logits.

The tone weights were already zero and remain zero. All other weights, biases, layers, and metadata are unchanged. No training or fitting was used.

Validation passed all 32 evidence labels and 50,000 constructed random and boundary inputs against the original model with the corrected inputs. The largest absolute logit difference was 4.27e-14; all decisions matched. Separate checks confirmed exact tone invariance and unchanged non-EU logits.
