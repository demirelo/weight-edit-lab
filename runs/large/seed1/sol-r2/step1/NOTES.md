# Weight edit

Set all first-layer weights from `tone_anger` (input index 3) to zero. Keep every other weight, every bias, the layer structure, and the JSON metadata unchanged.

For each first-layer unit, this removes only the term `tone_anger * weight`. Its preactivation therefore equals the original model's preactivation with `tone_anger = 0`. The same ReLU activations and later layers give the same output logit. This identity applies to all inputs. It preserves the original model exactly when `tone_anger = 0` and makes escalation independent of tone.

Verification: all 32 evidence labels pass. On 50,000 random valid inputs, edited logits exactly equal original logits with tone set to zero. Setting tone to either endpoint also leaves those logits unchanged. All other parameters and metadata match the input file. No training or fitting was used.
