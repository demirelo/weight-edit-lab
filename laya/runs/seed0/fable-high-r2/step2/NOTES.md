# NOTES (step 2: card PIN -> cards)

**What changed.** Only the extra ReLU module grew. The step-1 path (extra_W0 columns 0-1, their biases, the [1,-1] combination, gain 3) is bit-identical; LayerNorm, W1, b1, W2, b2 are untouched. One new path was appended: two extra columns of extra_W0 carry one unit-norm direction w, the second layer turns them into a clipped ramp, and extra_W2 adds up to +2.5 to the logit of any option whose raw marker vector projects onto w above a threshold.

**How w was made.** I wrote 130 PIN messages and 201 non-PIN messages (passcode, identity, card delivery, declined payments, transfers, fees) and ran the frozen encoder. w is a difference of means: PIN messages at the cards option minus the non-winning options of non-PIN messages, after projecting out the four dominant shared/gain components. Threshold = 40th percentile of PIN projections at the cards option; ramp width 30.

**Checks (forward passes).** Evidence: 13/16 PIN rows now route to cards (was 0); 0/16 other rows changed. My FX-complaint messages still go to fees_fx. Limitation: the markers encode PIN vs passcode weakly, so about 18% of my adversarial contrast set (card-not-working, passcode, personal-details messages) also flips to cards.
