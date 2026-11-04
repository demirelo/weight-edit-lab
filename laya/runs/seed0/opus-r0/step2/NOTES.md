# Step 2: card PIN -> cards

**Change.** Base scorer and the step-1 unit are unchanged. I added a second hidden unit to the extra
module: `logit += 33 * ReLU(w . m + b)`, with `b = -104.7`.

**Direction.** I wrote 201 templated PIN messages and 239 non-PIN messages. The non-PIN set
includes 144 minimal pairs, where "PIN" becomes passcode, password or login. I took PCA of all
their option vectors and scaled each of the top 350 components by its own spread. In those units,
`w` is a difference of means: the cards-option vectors of the PIN messages, minus all other
vectors. Unscaled differences did not separate.

**Threshold.** The threshold is 7.5 spreads above the mean of the "other" vectors. PIN messages
have a median near 10 spreads. The worst non-PIN message is near 6.5. The gain of 30 per spread
beats the step-1 unit's account_security boost (up to +63).

**Checks.** These sets are hand-written and were not used to build `w`.
- PIN messages to cards: 76/80 and 30/30 (were 14% and 17%).
- Non-PIN routes changed: 0/88 and 0/104. Training negatives: 0/239 changed.
- Evidence: 32/32 (was 17/32). Evidence labels were not used.
