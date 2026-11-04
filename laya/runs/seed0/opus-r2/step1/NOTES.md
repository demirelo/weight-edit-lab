# Step 1: exchange-rate complaints -> fees_fx

**Change.** I changed one hidden unit of the main scorer (unit 786). Before, it was nearly dead: W2 = 3.6e-6, with a largest logit effect of 1e-5. No other weights changed, and I added no extra module.

**Detector.** I wrote my own messages: 80 rate complaints, 99 disputes and other-department messages, and 64 neutral currency or fee questions. Each direction is a difference of means in post-LayerNorm space. The positive side is the fees_fx option vector of a complaint. The negative side is all other option vectors, plus the fees_fx vectors of the neutral questions. I first removed the top 10 or top 20 principal directions of my probes, which carry match strength, not topic. I averaged the two directions in z-units.

**Unit.** W1[:,786] = 10·u and b1 = -10·(m + 2.75), so it fires only above z = 2.75. W2 = 0.6 adds up to about +6 to the fees_fx logit. LayerNorm stays exact.

**Check (forward passes only).** 35/38 held-out handwritten complaints go to fees_fx. There were 0 flips on 273 non-target probes. Evidence went from 16/32 to 29/32, with no change on non-target rows.
