# Step 3: account eligibility (age, countries) -> account_security

**Change.** I repurposed two near-dead hidden units (1010, 48; each had |W2| < 4e-5). Units 786, 740, 771, 828 and 1006 from steps 1 and 2 are untouched. No other weights changed, and I added no extra module.

**Detector.** I wrote 328 eligibility messages and 378 others, including near-misses (transfers to countries, currencies, cards for family). The direction is a difference of means in post-LayerNorm space. The positive side is the account_security vector of eligibility messages. The negative side is all option vectors of non-eligibility messages, plus, with weight 0.3, the other options of eligibility messages. I removed the top 150 or 300 principal directions of the non-target vectors only, then averaged the two directions in z-units.

**Units.** Two sharp GELUs form a capped ramp: 0 below z = 3.5, rising to +4 logits at z = 5.5. It adds to the logit of any option whose vector fires.

**Check (forward passes only).** On a fresh set: 21/24 eligibility messages go to account_security. 0/47 unrelated messages flip; 3 "will my card work in <country>" questions move to account_security. Evidence: 16/32 to 27/32. PIN and exchange-rate probes: 0 flips.
