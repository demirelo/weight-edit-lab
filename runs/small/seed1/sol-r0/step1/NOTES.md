Set all 16 first-layer weights from `tone_anger` to zero. Keep every other weight, bias, layer, and metadata field unchanged.

The first-layer preactivation now excludes tone. Thus all hidden activations and the output logit are independent of tone for every input. This removes tone-driven escalation across the full input domain.

The edited model computes exactly the original model with `tone_anger = 0`. It preserves the original effects of impact, urgency, users affected, startup phase, and confidence at that reference tone.

No training, fitting, or optimization was used. Verification passed all 24 labelled examples. It also confirmed identical logits against the original model at zero tone on 50,000 random inputs, and identical logits across tone changes on those inputs, including tone endpoints 0 and 1.
