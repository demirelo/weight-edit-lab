I kept the original weights and added ReLU units and layers. No training or fitting was used.

Let f be the original logit, i the impact, and s the startup flag. The added units compute:

    d = ReLU(0.6 - i)
    g = ReLU(1 - 2^53 d)
    output = f - ReLU(f - 128(g + 1 - s))

The original logit has an analytic upper bound of 68.360 on the input domain, so 128 preserves allowed cases. For float64 inputs, every impact below 0.6 has d >= 2^-53. Thus startup noise produces min(f, 0). At impact >= 0.6, or outside startup, the original logit is preserved mathematically. All tone weights remain zero.

Limit: the literal requirement for every real input is impossible with continuous ReLU networks. The original logit is positive at some startup inputs with impact exactly 0.6. Continuity prevents preserving those positive values while rejecting every smaller real impact. This construction has a real-valued transition within 2^-53 below 0.6.

Validation passed all 24 evidence labels and 100,240 random/boundary cases, including adjacent floats around 0.6. Tone invariance was exact. Allowed-region logit differences were at most 2.85e-14.
