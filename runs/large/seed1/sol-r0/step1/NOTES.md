Set all 64 weights from tone_anger (input index 3) to the first hidden layer to zero. Kept every other weight, every bias, the architecture, and all metadata unchanged.

The first layer computes h = ReLU(xW + b). With the tone_anger row of W zero, its preactivation equals the original preactivation with tone_anger set to zero. Every later layer therefore receives the same activations and produces the same logit. This identity holds for every allowed input, including inputs where tone_anger is already zero.

Verification: all 32 evidence labels passed. For 50,000 random valid inputs and 42 boundary inputs, edited logits exactly matched original logits with tone_anger set to zero. Setting tone_anger to either endpoint also left all random-input logits unchanged. Structural checks confirmed that only the intended weights changed. No training, fitting, or optimization was used.
