# Step 3: eligibility questions go to account_security

**Change.** The main scorer and the 8 earlier extra units are unchanged. I added one parallel (block-diagonal) unit to the extra module: layer 0 gives `g = ReLU(f(x) - 0.7)`, layers 1-4 pass `g` through, and the last layer adds `9 * g` to the logit.

**Direction f.** I wrote about 490 messages: eligibility questions (age, children, countries, residency) and other questions from all five departments, with hard twins such as "ship my card to Canada". Two huge shared directions hide the topic signal, so raw mean differences fail. I took PCA axes (K=250) of my own vectors, computed without labels, and rescaled each axis to unit spread. In those units, f is the mean of eligibility messages' account_security-option vectors minus the mean of all other vectors, other options included. The scale is 0 at the "other" mean and 1 at the eligibility mean.

**Safety.** On non-account_security options, f stays at 0.58 or lower, below the gate. Other logits are unchanged.

**Checks.** Evidence: 10/16 fixed, 0/16 others changed. 52 fresh messages: 13/20 fixed, 0/32 changed, including PIN and FX-rate cases.

**Caveat.** This rescaling plus a mean difference is close to LDA.
