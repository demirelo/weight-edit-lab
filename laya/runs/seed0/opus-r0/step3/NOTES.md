# Step 3: age and country eligibility -> account_security

**Change.** Base scorer and the two earlier units are unchanged. I added a third hidden unit to the
extra module: `logit += 3 * ReLU(w . m + b)`, with `b = -10.89`.

**Direction.** I wrote three batches of messages: 217 eligibility questions (age limits, children,
supported countries, residency) and 189 negatives. The negatives include hard card-usage questions
(ATMs, shops, Apple Pay, delivery abroad), currency questions and other departments. I took PCA of
all option vectors and scaled the top 400 components by their spread. In those units, `w` is the
account_security-option mean of the eligibility messages minus the mean of all other vectors.
Account_security options of account_security negatives were left out, because a boost there is harmless.

**Threshold and gain.** The unit fires 6.5 spreads above the "other" mean. Eligibility messages sit
near 8 to 13. I chose these by hand with leave-one-batch-out checks.

**Checks** (`cv.py`, forward passes only):
- Held-out eligibility to account_security: 93%. Held-out negatives changed: 5/189.
- Fresh batch: 10/10 eligibility fixed, 1/29 negatives changed.
- Evidence: 31/32 (was 16/32). Step-1 and step-2 evidence: 0 routes changed.

Evidence labels were not used to build `w`.
