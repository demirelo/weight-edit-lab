# Tone-independent escalation

I set all 16 weights from `tone_anger` to the first hidden layer to zero. I left every other weight, bias, layer, and metadata field unchanged. No training or fitting was used.

For any input, the edited model computes exactly the original model with `tone_anger = 0`. Because tone has no remaining path to any hidden unit, changing tone cannot change the logit or escalation decision anywhere in the input domain. The model retains its original response to impact, urgency, and the other inputs at that baseline.

Validation: all 24 labelled examples pass. Forward-pass checks on 50,000 random inputs confirm tone independence and equality with the original model at zero tone. A parameter comparison confirms that only the 16 tone input weights changed.
