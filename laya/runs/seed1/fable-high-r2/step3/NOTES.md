# Step 3 notes

**Change.** The original scorer and the step-1 and step-2 pathways are untouched. I appended a third block-diagonal pathway (12 -> 3 -> 1 units) that adds `e3 = 6 * AND(slot gates, OR(topic gates))` to the logit.

- Units: PCA of my 480 messages (2400 marker vectors), each PC in units of its own standard deviation.
- Slot gates: four pairwise differences of means "account_security slot minus slot j" (PCs 2-63), each a ramp starting above the maximum of slot j. Their AND is zero on every other slot, so only the account_security logit can move.
- Topic gates (account_security slot, PCs 8-255): "my 230 eligibility messages minus my 250 other messages", OR "my 48 card-worded eligibility messages minus my 95 cards messages". Each ramp starts at the 99th percentile of my contrast messages. OR is `min(1, a+b)`, AND is `relu(a+b-1)`.

**Checks (final.py).** Evidence: 15/16 eligibility messages now route to account_security, 0/16 others changed. Step-1 and step-2 evidence: 0 changes. Split-half on my messages: 86% of held-out eligibility messages flip, 3% of held-out near-neighbour contrasts change, no leak onto other slots. Only means, standard deviations, percentiles and forward passes were used.
