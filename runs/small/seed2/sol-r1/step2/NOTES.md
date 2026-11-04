I retained the original hidden units and their zero tone weights. Added ReLU units compute the impact deficit d = max(0, 0.6 - impact), the startup complement q = 1 - startup_phase, and g = max(0, d - q). Thus g is zero outside startup and at impact >= 0.6.

The output is f - max(0, f - 256 + 2^64 g), where f is the original logit. An analytical bound gives |f| <= 155.081. When g = 0, the output equals f. For any float64 impact below 0.6 during startup, g >= 2^-53, so the output is negative. Tone has no effect. All weights follow these formulas; no training or fitting was used.

Limitation: exact compliance for every mathematical real input is impossible for a finite continuous ReLU network when f is positive at the cutoff. The construction satisfies the cutoff for float64 inputs, including 0.6 and its adjacent values; ideal real arithmetic has an unavoidable transition interval smaller than float64 spacing.
