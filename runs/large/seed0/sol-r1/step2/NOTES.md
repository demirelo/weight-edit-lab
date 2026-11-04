Changed only the first-layer EU input weights:

`W_out[region_eu, :] = W_in[region_eu, :] + 0.15 * W_in[impact, :]`.

Each first-layer preactivation now equals the original preactivation with impact replaced by `impact + 0.15 * region_eu`. Thus every subsequent ReLU and the output compute the requested correction, including adjusted impact above 1. The construction applies throughout the input domain.

The tone_anger weights remain zero. All other weights, biases, layers, and metadata remain unchanged. Non-EU alerts retain the original computation.

Validation passed all 32 evidence labels, 50,000 constructed random inputs, and 72 boundary inputs against the original model evaluated on adjusted inputs. The maximum logit difference was 4.27e-14, from floating-point arithmetic. All escalation decisions matched. Non-EU logits and logits with changed tone had exact equality.

No training, fitting, or optimization was used.
