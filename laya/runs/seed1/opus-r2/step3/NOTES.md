# Step 3 notes

**Change.** I kept all existing weights and added one AND-gate group to the extra module (8 step units, 1 AND unit, output +0.6). It fires only on the account_security option vector, and only when:

- **Option gate.** W0 columns 40/44/46, copied from the disabled third group (output weight 0), with thresholds raised by 2. They pass on AS for 77–92% of my messages, and on other options for ≤5%.
- **No AS spike.** The projection on the mean (AS − transfers) offset of my identity messages stays under 14M. PIN and identity messages spike above 16M, so PIN routing stays as before (correction 2).

**Why so small.** Eligibility messages trigger no option's match spike. Their AS and transfers vectors are nearly identical, and every content direction I derived reached only ~0.6–0.75 AUC. So the boost acts mostly by margin; past +0.6, harm rises steeply.

**Measured on my messages.** Eligibility routed to AS: 45%, up from 3%. Other routes changed: 2.8%. PIN and FX unchanged. Evidence: 23/32, up from 16/32.

**Known gap.** scorer_in already fails correction 2 on 10 of my 13 PIN phrasings. I did not fix that.
