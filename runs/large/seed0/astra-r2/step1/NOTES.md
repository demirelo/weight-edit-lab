# Changes and checks

Set all 64 weights in the first-layer row for `tone_anger` (input index 3) to zero. Kept every other weight, every bias, the layer structure, and the JSON metadata unchanged. No training or fitting was used.

For any input, the edited first-layer preactivation equals the original first-layer preactivation with `tone_anger` set to zero. All later layers are unchanged. Thus the final logit and escalation decision equal those of the original model with `tone_anger = 0` for every valid input. Inputs that already have zero tone retain their original behavior.

Validation: all 32 evidence labels pass. On 50,000 random valid inputs, edited logits exactly match the original logits with tone set to zero. Setting tone to either endpoint (0 or 1) also leaves these logits unchanged. Structural checks confirm that only the intended weight row changed.
