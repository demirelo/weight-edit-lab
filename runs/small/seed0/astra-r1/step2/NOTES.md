I kept the original 16 hidden units and their zero tone weights. I added three units: p = ReLU(impact - 0.6), n = ReLU(0.6 - impact), and q = ReLU(1 - startup_phase).

Let f be the original logit and C = 2^30 * (p - n + q). The next hidden layer computes ReLU(f), ReLU(-f), and ReLU(f - C). The linear output is f - ReLU(f - C) = min(f, C). All weights follow this formula; no training or fitting was used.

During startup, impact below 0.6 gives C < 0, so escalation is blocked. Above 0.6, decisions are preserved. Outside startup, C exceeds the original logit's upper bound of 83.539, so the original logit is preserved, subject to floating-point roundoff. Tone has no effect.

Exact compliance is impossible at impact = 0.6: the original logit can be positive there, but continuity requires a nonpositive output after blocking every smaller impact. This edit outputs zero there. Startup logits can also change within 0.000000078 above the threshold, without changing decisions.

Checks passed: 24 evidence rows, 50,000 random decisions, tone invariance, and 224 boundary/domain cases with the stated equality exception.
