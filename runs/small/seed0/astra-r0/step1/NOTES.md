# Weight edit

I set all 16 first-layer weights from `tone_anger` to zero. I kept all other weights, biases, layers, feature order, and metadata unchanged.

For every input, the edited model computes the original model with `tone_anger = 0`. No path from tone to the output remains, so tone cannot change the logit or escalation decision anywhere in the input domain. The original calculations for impact, urgency, and the other inputs remain intact at this neutral-tone baseline.

Validation: all 24 evidence labels pass. On 50,000 constructed random inputs, edited logits exactly match original logits with tone set to zero. Changing tone to 0, 0.5, or 1 leaves every edited logit unchanged. All other model parameters are unchanged.

I used no training, fitting, or optimization.
