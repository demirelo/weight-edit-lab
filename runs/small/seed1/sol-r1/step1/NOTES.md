Set all 16 weights from tone_anger to the first hidden layer to zero. Kept all other weights, biases, layers, and metadata unchanged. No training or fitting was used.

The network now computes exactly the original network with tone_anger fixed at zero. Because tone has no remaining path to any hidden unit, it cannot affect the logit or escalation decision anywhere in the input domain. The original dependence on impact, urgency, users_affected, startup_phase, and confidence remains at that zero-tone baseline.

Validation: all 24 labelled examples pass, including the 12 changed decisions and 12 unchanged decisions. On 50,000 random valid inputs, logits equal the original network evaluated with tone zero. Changing tone to zero, one, or another random value leaves the edited logits identical. These checks supplement the structural guarantee of tone independence.
