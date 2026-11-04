# Weight edit

Set all 16 first-layer weights from `tone_anger` to zero. Keep every other weight, every bias, the network structure, and the JSON metadata unchanged.

Each hidden unit now computes the original activation with `tone_anger = 0`. Thus, for every input, the edited logit equals the original logit at the same input with zero anger. Tone cannot affect any hidden activation or the escalation decision. The original response to the other five features remains intact at this baseline.

Checks passed: all 24 labelled examples; exact logit equality to the original zero-anger baseline on 50,000 constructed random inputs; and exact tone invariance at five tone values for each input. The weight comparison confirmed that only the 16 tone weights changed.

No training, fitting, or optimization was used. All weights were selected by direct reasoning.
