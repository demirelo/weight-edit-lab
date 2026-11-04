# Step 1: wrong exchange rate -> fees_fx

**Change.** Base scorer unchanged. Added a one-unit extra ReLU module on the raw marker
vector `m`: `logit += 5 * ReLU(v . m - 5)`.

**Why.** Marker vectors have about 6 effective dimensions, which carry the option-fit signal
the scorer reads. Message content sits in the low-variance remainder. I removed the top 12
principal directions of my own messages' vectors. In the remainder, `v` is a difference of
means: the fees_fx-option vectors of 105 rate complaints I wrote (card payments, cash
withdrawals), minus all vectors that must not rise. Those are all options of 178 other messages
I wrote, plus the non-fees options of the complaints. Fee/FX questions were excluded, because
a boost there is harmless.

**Threshold and gain.** Chosen by hand with 3-fold checks over my three message batches.
- Held-out complaints now fees_fx: 33/35, 28/30, 37/40.
- Hard negatives changed: 3/64, 2/40, 4/74. These are mostly "charged the wrong amount" or
  exchange-rate questions the old model sent to cards.
- Evidence: 29/32 (was 16/32). No evidence message moved off its correct label.

Evidence labels were not used to build `v`.
