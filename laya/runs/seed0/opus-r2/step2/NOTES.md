# Step 2: card PIN messages -> cards

**Change.** I repurposed four near-dead hidden units (740, 771, 828, 1006; each had |W2| < 3e-5). No other weights changed, and I added no extra module. The step-1 unit 786 is untouched.

**Detectors.** I wrote 189 PIN messages and 447 non-PIN messages (passcode, login, ID, address, age, cards, other departments), including minimal pairs ("PIN" vs "passcode"). Each detector is a difference of means in post-LayerNorm space. The positive side is the cards (or account_security) vector of PIN messages. The negatives are the same vector of non-PIN messages, plus, with weight 0.1, the other option vectors. I removed the top 30/40/60/80 principal directions, which carry match strength, and averaged the four directions in z-units.

**Units.** Two sharp GELUs per detector form a capped ramp: 0 below z = 2.5, rising to 4 logits at z = 3.0. One pair adds to the cards logit; the other subtracts from the account_security logit.

**Check (forward passes only).** Held-out handwritten PIN: 46/67 go to cards (before: 1/67). Flips: 2/447 build and 7/129 held-out non-PIN probes, mostly age questions. Evidence: 16/32 to 27/32, with no change on non-PIN rows. Exchange-rate complaints route as before.
