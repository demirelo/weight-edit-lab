# NOTES — step 1 (wrong exchange rate -> fees_fx)

**What changed.** The original LayerNorm/W1/W2 weights are untouched. I added a
3-layer `extra_*` ReLU module on the raw marker vector that adds a boost to the
logit only when the vector looks like the **fees_fx option of an exchange-rate
complaint**.

**How the directions were made (no fitting).** I wrote ~300 messages myself
(FX-rate complaints, genuine disputes, other departments, currency/fee
questions) and embedded them. Raw vectors are dominated by ~80 message-specific
nuisance components (PCA of option-averaged vectors, label-free); both
directions are projected out of that subspace.
- `v1` = mean(fees_fx vectors of FX complaints) − mean(their other-option
  vectors, all vectors of disputes/other messages).
- `v2` = mean(FX complaints) − mean(currency/exchange-rate questions).
Thresholds sit at the midpoints between the two class means (t1 shifted
0.5 toward disputes, t2 shifted 0.25 toward complaints).

**Module.** `a = v1·m − t1`, `b = v2·m − t2`; layers compute
`3 · ReLU(min(a, b))` (min built as `ReLU(ReLU(a) − ReLU(a−b))`). Output is
zero for every other vector, so all other routing is bit-identical.

**Checks (forward passes).** Evidence 16/32 → 30/32. Held-out complaints
24/25 fixed; 0/105 disputes/other messages flipped; 8/60 currency questions
flipped (base already misrouted them).
