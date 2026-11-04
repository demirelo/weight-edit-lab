# Step 3: age/country eligibility -> account_security

**What changed.** The main scorer (LN, W1, W2) is not changed. I added a parallel path to the extra ReLU module. The old path keeps its own weights. With G=0, the logits are exactly the same as scorer_in.

**How it works.** I subtract the large shared offset from each marker. Then I remove the top principal directions of my own unlabelled markers (12 for the gate, 64 for the content). Each detector uses `d·x / |x|_1`, built from `relu(±x)`, so marker scale does not affect it.
- Gate `o`: mean(account_security markers) − mean(other markers).
- Eligibility `e`: mean(my age/country messages) − group-balanced mean(cards, fees, disputes, transfers, security, look-alike questions).
- Veto `c`: mean(currency-support questions) − mean(eligibility questions).

Output: `+4 · relu(clamp(gate) + clamp(e) − 1 − clamp(c))`, only on the account_security logit. All directions are differences of means of messages I wrote. I set the thresholds by hand from forward passes.

**Results (held-out messages I wrote).** 32/52 eligibility messages now go to account_security (before: 2). 3/117 other messages changed. Evidence: 26/32 correct (before: 16). PIN and exchange-rate checks match scorer_in.
