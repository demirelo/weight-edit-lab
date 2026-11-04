The original hidden units, output weights, and output bias stay unchanged. Two new units compute r = ReLU(impact - t) and startup_phase, where t = 0.5999999999999999, the float64 value immediately below 0.6. A new ReLU layer copies the original activations and computes p = ReLU(128 * startup_phase - 2^60 * r). The output is the original logit minus p.

Outside startup, p is zero. During startup, every representable impact below 0.6 gives p = 128; every representable impact at or above 0.6 gives p = 0. The original logit has a conservative upper bound of 68.36 on the input domain, so subtracting 128 always prevents escalation. All tone weights remain zero.

All added weights follow these formulas. No training or fitting was used.

Real-number limitation: finite ReLU networks are continuous. The requested strict cutoff cannot preserve a positive logit at exactly 0.6 while preventing escalation arbitrarily close below it. This construction satisfies the cutoff for float64 inputs used by model.py; its transition lies between adjacent float64 values.
