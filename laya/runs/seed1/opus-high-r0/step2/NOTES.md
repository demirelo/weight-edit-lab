# Step 2: card PIN -> cards

The original scorer and the step-1 module are unchanged. The step-1 output now passes through one extra ReLU layer with weight 1, which keeps it the same. Beside it, I added two gates: a cards bonus (up to +4) and an account_security penalty (up to -4).

**Directions** (only messages I wrote: 180 PIN, 245 non-PIN):
- PIN-ness on the cards vector, and separately on the security vector. Each is the PIN mean minus the non-PIN mean, with the top 120 within-group spread axes projected out. A plain mean difference was swamped by those axes (AUC 0.6-0.8).
- Option identity (cards vs each other option, security vs each other option), built the same way.

**Units:** 1024 units ReLU(x_i - mean) sum to a scale signal that tracks the LayerNorm std within about 1%. Each direction is shifted so its threshold sits near 0, so scale errors barely move the decision. Each gate is ReLU(scale - sum of shortfalls), a bounded soft AND.

**Checks** (forward passes): new PIN messages 26/30 and 18/20 fixed. Non-PIN messages changed: 0/46 and 0/75. Evidence 29/32 (was 16). Step-1 evidence unchanged.
