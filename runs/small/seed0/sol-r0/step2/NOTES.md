Kept the original 16 hidden units and their weights. Tone weights remain zero.

Added r = ReLU(startup_phase - impact + (0.6 - 1)) and one hidden layer. For original logit f, the new output is min(f, 128 - 2^61*r). An interval bound gives f <= 79.964431 across the input domain.

Outside startup, or at impact >= 0.6, r = 0 and the original decision remains. For float64 startup inputs below 0.6, the smallest positive r is 2^-53. The cap is therefore at most -128, which prevents escalation. All weights follow these formulas; no training or fitting was used.

Real-number limit: finite ReLU networks are continuous. The original model has positive logits at startup impact 0.6, so no such network can reject every real impact below 0.6 while preserving those boundary logits. This edit meets the threshold at float64 precision; an infinitesimal interval of unrepresentable real inputs can violate the rule.

Checks passed: 24 evidence labels, 50,000 random inputs, 224 boundary/corner inputs, 60,000 threshold inputs, and 400,002 gate checks. Tone remained invariant. Preserved logits differed by at most 8.9e-16 in these checks.
