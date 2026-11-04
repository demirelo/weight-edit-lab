# Step 2 edit: card PIN -> cards

**Change.** Scorer weights untouched. The step-1 module is kept exactly; a second block is added beside it (block-diagonal: 1024 -> 9+10 -> 2 -> 1). The new block adds up to +12 to the **cards option's** logit only for PIN messages.

**Features** (difference of means of marker vectors of messages I wrote, in standardised PC 3-300 coordinates from an unlabelled SVD; mean-free, so raw `M.q + c`):
- I: cards option vs the other four options (hard gate, weight 4),
- Pn: PIN vs non-PIN messages,
- Pp: minimal pairs ("my PIN is blocked" vs "my passcode/password/card... is blocked"),
- Ps: PIN vs passcode / security messages,
- Po: PIN vs disputes/transfers/fees messages.

Each is a clipped ramp from the 90th percentile of its negatives to the 10th percentile of its positives. Unit = relu(sum of 4 PIN ramps + 4*I - 4 - 2), times 6.

**Checks (forward passes).** Evidence 15/32 -> 29/32 (14/16 PIN). Held-out PIN probes 20/20. Held-out general set (63, incl. passcode look-alikes and 8 wrong-rate messages): 0 changed. Non-cards option logits change by < 1e-5.

**Disclosure.** Threshold and boost were picked by forward-pass checks.
