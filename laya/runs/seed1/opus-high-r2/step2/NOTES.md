# Step 2: card PIN -> cards

**Original scorer and the step-1 module are unchanged.** I added a second ReLU module beside the step-1 module (block-diagonal layers, outputs summed). It adds up to +8 to the cards logit only. It outputs exactly 0 on every other option.

**Detectors** (cards option, same method as step 1): mean differences of my own messages in 512 unit-variance PCA axes (label-free). Each check has 0 = halfway between the two means:
1. PIN messages vs everything else, all options
2. vs passcode, login and identity messages
3. cards option vs the other options of PIN messages
4. vs ~75 other banking request types
5. cards option vs other options, all messages (stops leaks to fees_fx)

The module fires only when all five are > 0 (min built from ReLUs), then a steep ramp capped at +8. Step 1's module got one identity layer so the depths match.

**Checks** (held out, my own and evidence): 53/58 PIN messages go to cards; 0/714 other messages change route; the logit of no other option ever moves. Evidence: 31/32. Step-1 fees_fx results are identical.

**Not used:** evidence labels, training, solvers. A leak check passed.
