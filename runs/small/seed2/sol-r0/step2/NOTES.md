I retained all original hidden units and their weights, including the zero tone weights. I added two gate units and a ReLU layer. No training or fitting was used.

Let f be the original logit, t the binary64 value immediately below 0.6, and s the startup flag. The gate is g = ReLU(2^64 * (impact - t)) + 128 * ReLU(1 - s). The output is f - ReLU(f - g), implemented with positive and negative parts of f.

The original logit has an analytical upper bound below 104 on the input domain. Outside startup, g is at least 128, so the original logit passes through. During startup, every binary64 impact below 0.6 gives g = 0 and a nonpositive output. At impact 0.6 or above, g is at least 2048, so the original logit passes through. Tone remains irrelevant.

Mathematical limit: a continuous ReLU network cannot enforce this strict cutoff for every real input while retaining a positive logit at exactly 0.6. This construction satisfies the cutoff for binary64 inputs; its real-valued transition lies between adjacent floating-point values.
