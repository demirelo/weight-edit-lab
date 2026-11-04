Inferred rule: tone_anger must have no effect on escalation at any level. For every input x, use F(x0), where x0 is x with tone_anger set to zero. Escalate only if this logit is strictly greater than zero.

The query labels are 0, 0, 0, 1, 1. They select candidate 1 and reject both the proposed linear subtraction and the proposed anger threshold.

I set the 64 tone_anger weights in the first layer to zero. All other weights, biases, layers, and metadata remain unchanged. The first layer now computes exactly the same values as the original first layer given x0. Thus every later layer computes F(x0) for every valid input. Inputs with zero anger retain their original logits. No training or fitting was used.

Validation: all 32 evidence labels and all 5 query labels match. On 50,000 random valid inputs, edited logits exactly equal original logits with anger zeroed. This equality also holds with anger fixed at 0, 0.1, 0.249, 0.25, and 1. An edit audit confirms that only the 64 intended weights changed.
