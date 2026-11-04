Changed only the first-layer EU weight row (index 8):

W_out[8, :] = W_in[8, :] + 0.15 * W_in[0, :].

For every first-layer unit, this replaces the impact contribution with
(impact + 0.15 * region_eu) * W_in[0, :]. Thus the entire network computes
the original network with adjusted impact. No clipping occurs, so EU impact
can reach 1.15. Non-EU inputs retain their original computation.

The tone_anger row (index 3) remains identically zero. All other weights,
all biases, the architecture, and metadata remain unchanged. No training
or fitting was used.

Verification: 50,000 random inputs and 1,024 boundary inputs matched the
adjusted-input reference within floating-point roundoff, with identical
escalation decisions. Random checks also confirmed exact non-EU logits
and tone invariance.

Evidence: 31/32 labels match. Example 9 (CSV line 10) has label 1, but the
original network with the required impact adjustment yields logit
-0.12744282298467907. The edited network agrees. This label conflicts with
the specified transformation; no example-specific exception was added.
