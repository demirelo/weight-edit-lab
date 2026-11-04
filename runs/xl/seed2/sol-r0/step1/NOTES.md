# Weight edit

Set all outgoing weights from `tone_anger` (input index 3) to zero in the first layer. Preserve every other weight, every bias, all layers, and the model metadata.

The first layer computes `X @ W + b`. Removing the `tone_anger` row contribution gives exactly the first-layer preactivation of the original model with `tone_anger = 0`. All later computations therefore give the same logit and escalation decision as that corrected input, for every valid alert.

Verification: all 32 evidence labels pass. On 50,000 random valid inputs, edited logits equal original logits with `tone_anger = 0`, with zero observed error. Setting anger to 1 also leaves edited logits unchanged. Checks pass for all eight binary-feature combinations at both continuous-feature limits. Structural checks confirm that only the intended first-layer weights changed. No training or fitting was used.
