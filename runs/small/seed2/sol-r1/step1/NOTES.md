# Weight edit

Set all 16 first-layer weights from `tone_anger` to zero. Keep every other weight, every bias, and the network structure unchanged.

Tone now has no path to the output. For every valid input, the edited model computes the original model with `tone_anger = 0`. This removes the tone contribution and preserves the original response to the other five features at that reference value.

Validation: all 24 labelled examples pass. Forward checks on 50,000 random inputs confirm equality with the original model at zero tone and confirm that changing tone does not change the edited output. Parameter checks confirm that only the 16 tone weights changed. No training, fitting, or optimization was used.
