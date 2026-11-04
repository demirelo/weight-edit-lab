# NOTES (step 2): card PIN -> cards

**Change.** Four hidden units that contributed <1e-3 to any logit on my corpus (columns 234, 534, 740, 972) now hold two threshold detectors, each a pair of GELU units giving a clipped step. Step-1 units (38, 48, 52) and all else untouched; no extra module.

- Detector A on the account_security option vector: "PIN content" -> account_security logit -8.
- Detector B on the cards option vector: "PIN content" -> cards logit +2 (breaks the cards/disputes tie).

**Directions** (no fitting; 300 messages I wrote, embedded with embed.py). Plain mean differences fail: 99% of marker variance is two shared axes. So I measure in whitened coordinates: PCA of my 110 generic messages' LayerNorm vectors, top-100 components scaled to unit variance. Content = mean of my 70 PIN messages minus mean of generic messages, same option. Option identity = mean of that option's vectors minus the others; added with weight 3 as a gate. Thresholds at the 99%/98% quantile of my non-targets, gains from forward passes.

**Measured** (held out). 20 new PIN messages: 14/20 -> cards. Evidence: 29/32 correct (was 15). 276 non-PIN controls across all Banking77 intents: 2 changed. Exchange-rate messages unchanged.
