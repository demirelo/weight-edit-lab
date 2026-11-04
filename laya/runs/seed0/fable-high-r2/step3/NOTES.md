# Step 3: eligibility (age / country) -> account_security

**What changed.** Only the extra ReLU module grew: `extra_W0` 1024x4 -> 1024x12, `extra_W1` 4x2 -> 12x5,
`extra_W2` 2x1 -> 5x1. The base scorer and the old columns from steps 1-2 are untouched.

**How (no training).** I wrote ~440 eligibility messages (age limits, supported countries, residency /
"can I get a card in X") and ~410 controls, and embedded them. From all these vectors I took the principal
directions: the top 32 carry the model's own match score and were dropped; the next 480 were each scaled to
unit spread. There, three content directions are plain differences of means (age, country availability,
residency) between my eligibility messages and my controls, read on the account_security option vector. A
fourth is the within-message mean difference "account_security option minus the others" (identity gate).
Each direction is a two-ReLU clipped ramp; thresholds are the 99.5th percentile of my controls plus 0.25 sd.
Layer 2 ANDs each content ramp with the gate; layer 3 adds up to 3.5 to the account_security logit only.

**Checks.** Evidence 15/32 -> 26/32. 156 realistic non-eligibility messages, never fitted: 0 route changes.
Other options' logits are exactly unchanged; steps 1-2 hold.
