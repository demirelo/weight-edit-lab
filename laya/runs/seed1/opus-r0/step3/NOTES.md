# Step 3 edit: age / country eligibility -> account_security

**Change.** Scorer weights untouched. Step-1 and step-2 blocks kept exactly; a third block is added beside them (1024 -> 19+12 -> 3 -> 1). It adds up to +9.6 to the **account_security option's** logit only for eligibility questions.

**Features** (difference of means of marker vectors of ~200 messages I wrote, in standardised PC 3-450 coordinates from an unlabelled SVD, mapped back to raw `M.q + c`):
- I: account_security option vs the other four options (gate, weight 4),
- E: eligibility vs all my negatives,
- Ec: vs card messages (delivery abroad, ordering, PIN),
- Es: vs other account_security (ID checks, passcode, closing),
- Eo: vs fees/transfers/disputes,
- El: vs near look-alikes (Apple Pay, stolen phone, card shipping).

Each is a clipped ramp from the 90th percentile of its negatives to the 10th percentile of its positives. Unit = relu(5 ramps + 4*I - 7.8), times 8.

**Checks (forward passes).** Evidence 16/32 -> 32/32. Step-1 and step-2 evidence: 0 changed. Held-out eligibility probes 23/24. Held-out negatives (112): 1 changed ("Can I have a joint account?"). Non-AS logits unchanged.

**Disclosure.** Threshold, boost and PC range were picked by forward-pass checks.
