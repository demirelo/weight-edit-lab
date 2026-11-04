# Changes

Set all 16 first-layer weights from `tone_anger` to zero. Keep all other weights, biases, layers, and metadata unchanged. No training or fitting was used.

Each hidden preactivation now excludes tone. Thus, tone cannot change any hidden activation or the output logit, for any input. The edited model computes exactly the original model with `tone_anger = 0`. This preserves the original neutral-tone decision rule and all remaining feature paths.

# Checks

All 24 labelled examples pass, including the 12 near-miss cases. On 50,000 constructed random inputs, output logits equal the original model's neutral-tone logits exactly. Setting tone to 0, 0.25, 0.5, 0.75, or 1 leaves those outputs unchanged. A structural comparison confirms that only the 16 tone weights changed.

The hidden test set was not available. These checks use forward passes only.
