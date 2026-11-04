# Weight edit

I set all 16 weights from `tone_anger` to the first hidden layer to zero. I kept all other weights, biases, layers, and metadata unchanged. I used no training or fitting.

For every input, the edited model computes the original model with `tone_anger = 0`. Thus, tone cannot affect the logit or the escalation decision anywhere in the input domain. The model retains its original response to impact, urgency, and the other inputs at zero tone.

Validation: all 24 labelled examples pass. Forward checks on 50,000 random inputs and all 64 input corners confirm equality with the original model at zero tone. Changing tone leaves the edited logits unchanged. These checks use constructed inputs, not the hidden test set.
