I kept the original hidden units and zero tone weights. I added ReLU units that apply a startup cap to the original logit f:

    t = nextafter(0.6, 0) = 0.5999999999999999
    cap = 2^60 ReLU(impact - t) + 128 ReLU(1 - startup_phase)
    output = f - ReLU(f - cap) = min(f, cap)

The original weights give a global upper logit bound of 83.539. Outside startup, cap is at least 128. During startup, cap is zero for every binary64 impact below 0.6, and at least 128 for impacts at or above 0.6. Thus the cap blocks startup noise and preserves other decisions. Tone has no effect. All weights come from algebra; no training or fitting occurred.

Exact compliance over real numbers is impossible: ReLU networks are continuous, but the requested rule retains positive boundary logits. This construction has a real-number transition between t and 0.6; no binary64 input lies there.

Checks passed: 24 evidence labels, 50,000 random inputs, 160 boundary/corner inputs, and exact tone invariance. Preserved logits differed by at most 3.56e-14 from floating-point arithmetic.
