# Step 2: card PIN -> cards

**Unchanged:** main scorer and the step-1 unit (fees_fx rate fix).

**Added:** one AND-unit in the extra module, +3 to the cards logit. It fires when 11 clipped conditions all hold on one option vector:

- 8 option gates: "cards option, not option j", in two PC bands (2-15, 15-60). Direction = mean cards vector minus mean option-j vector over all my messages.
- 3 PIN detectors on the cards vector, after removing the top PCs: PIN vs my account_security-routed messages, PIN vs all my non-PIN messages, and minimal pairs (same sentence, "PIN" vs "passcode"/"password").

Thresholds are percentiles of my PIN messages. A second unit (account_security penalty) has weight 0. It is inert.

**Why so careful:** the encoder hardly separates "PIN" from "passcode" (linear AUC about 0.8). Single-band gates leaked the bonus onto other options.

**Data:** about 470 messages I wrote. Evidence used only for checks.

**Results (forward passes):**
- Final unseen set: PIN to cards 1 -> 7 of 20. 1 of 50 non-PIN changed (a passcode message).
- Tuning sets: 4 -> 30 of 65; 3 of 140 changed.
- Evidence: 16 -> 21 of 32.
- Rate complaints are unchanged.
