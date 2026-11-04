# NOTES (step 3): account eligibility (age, country) -> account_security

**Change.** Two hidden units that contributed <1e-3 to any logit on my corpus (columns 361, 391) now hold one clipped threshold detector on the account_security option vector: "eligibility content" -> account_security logit +3. Step-1 units (38, 48, 52), step-2 units (234, 534, 740, 972) and everything else are untouched; no extra module.

**Direction** (no fitting; 120 new messages I wrote, embedded with embed.py, plus my step-2 corpora). Whitened difference of means: PCA of 253 generic messages' LayerNorm vectors, top-100 components scaled to unit variance. Content = mean of my 60 eligibility messages minus the generic mean. Threshold at the 99% quantile of non-target scores; gain and ramp width from forward passes. Implementation checked against the intended step (max error 0.01).

**Measured** (held out). 20 new eligibility messages: 16/20 -> account_security. Evidence: 27/32 correct (was 14). 40 near-confusers (card delivery/acceptance abroad, currencies): 3 changed. 253 other controls: 2 changed. Step-1 and step-2 messages route as before.

**Flag.** Step-1 unit 38 is an unclipped ramp (up to +70 on identity-verification messages). It flips nothing on my 502 messages, so I left it.
