I added three ReLU input layers and kept every original weight and bias unchanged. No training or fitting was used.

Let u be urgency and c be confidence. The new layers compute:

d = ReLU(2^55 * (0.4 - c))
r = ReLU(u - d)
u_adjusted = 2*u - r

All other inputs pass through unchanged. For c >= 0.4, d is zero, so urgency stays unchanged. For binary64 c < 0.4, d is at least 2, so urgency doubles. This includes the adjacent representable confidence values and the exact Python threshold. The original network then evaluates the adjusted inputs, preserving the earlier corrections.

Finite ReLU networks are continuous. In ideal real arithmetic, this construction has a transition interval of width at most 2^-55 below the stored threshold. No binary64 confidence value lies inside that interval.

Checks passed: 32/32 evidence labels; exact reference logits on 50,000 random inputs and 6,000 boundary inputs; tone invariance; critical override; unchanged original layers.
