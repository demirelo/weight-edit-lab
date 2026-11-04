# Manual weight edit

I kept the original 16 hidden units and their weights. Let f be the original logit, i the impact, and s the startup flag. I added ReLU units that compute:

- r = ReLU(i - a), where a = 0.5999999999999999, the float immediately below 0.6.
- t = ReLU(1 - s).
- g = 2^60 r + 128 t.
- Output = f - ReLU(f - g) = min(f, g).

Additional units carry f as ReLU(f) and ReLU(-f). An analytic bound gives f <= 103.54 throughout the input domain. Outside startup, or at impact >= 0.6, g >= 128, so the original logit is preserved. During startup, impact <= a gives g = 0 and prevents escalation. All tone weights remain zero.

Exact compliance over real inputs is impossible: ReLU networks are continuous, while the requested decision has an included positive boundary. The only possible exception lies between a and 0.6, about 1.11e-16 wide; no float64 input lies there.

Weights were derived directly. No training or fitting was used.

Checks passed: 24 examples, 100,000 random decisions, and 648 boundary decisions. Unaffected logits differed by at most 3.56e-14 from floating-point rounding.
