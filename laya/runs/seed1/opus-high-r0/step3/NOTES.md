# Step 3: eligibility -> account_security

**Changed:** only the extra module. I added a parallel path, block-diagonal to the old one. Where it is silent, logits are bit-identical.

**Why this shape:** marker vectors are dominated by a few huge "option match" components. Plain mean-difference directions separated eligibility poorly (AUC ~0.6). After I remove the top principal components of my own messages and L1-normalise the residual, the signal appears.

**Path:**
- Layer 0: relu(+r), relu(-r) of the residual r (40 PCs removed for the concept, 10 for the slot). Their sum gives |r|_1, so the tests below are scale-free.
- Layer 1: clipped hinges for three tests. Each direction is a difference of means over messages I wrote: age questions vs. non-eligibility messages, country questions vs. the same, and the AS option vs. the other options. Thresholds sit between the class means. The concept gate saturates at the typical positive.
- Layer 2: AND(concept, AS-option) for age and for country.
- Output: +1 logit per AND unit.

**Checks (forward passes):** held-out probes 34/56 eligibility -> AS (was 1), 3/224 other messages changed. Evidence 6/16, 0/16 others changed. All 29 PIN/exchange-rate probes unchanged.
