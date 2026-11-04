# Step 1 notes

**Change:** one dead hidden unit of the main scorer (unit 234; its pre-activation is at most -4.1 on every vector I tested, so it gave about 0 output) is rewired as a gated detector. No other weights changed. No extra module.

**Direction:** in LayerNorm output space. Mean of the fees_fx option vectors for ~190 bad-rate complaints I wrote (card payments and cash withdrawals), minus the equal-weight mean of 10 "rest" groups: the other options of those complaints, every option of ~480 other messages I wrote (all banking intents), and currency questions as their own group. The top principal directions of all my vectors (no labels used) carry most of the variance and hide the signal. I strip them from the direction, averaged over cutoffs 12–30.

**Gate:** threshold = 99.5th percentile of non-target projections. Slope gives +4 logits to fees_fx at the median complaint. GELU with a large input scale acts as ReLU.

**Checks (forward passes only):** new held-out complaints routed to fees_fx went from 27% to 70%. Evidence accuracy went from 50% to 94%. Unchanged routing: 99.3% of a broad 300-message set, 95.6% of a hard-negative set. Remaining flips are mostly other currency questions.
