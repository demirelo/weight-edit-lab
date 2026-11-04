# Step 3 notes: eligibility (age, country, residency) -> account_security

The original scorer and the step-1 (exchange rate) and step-2 (PIN) units are untouched; the new units are appended to the extra module (layer 1: 6 -> 14 units, layer 2: 2 -> 4) with zero cross-terms.

Direction set: 834 eligibility messages I wrote (templated, short/sloppy, and "can I get a card if I live in X" forms) and 1854 contrast messages (cards abroad, card delivery, currencies, transfers, identity, passcode, plus my step-2 PIN and account-security sets). The PIN contrast was necessary: a first direction fired on blocked-PIN messages.

Two units on the account_security option only, each an AND of content and option gate (as in step 2). Content = variance-normalized mean difference of account_security-option vectors in a label-free PC basis (PCs 7-1024). Unit A: general eligibility, bonus 5 * clip(zA - 0.2, 0, 1.2). Unit B: card-phrased eligibility, built from card-only subsets so the "card" feature cancels, bonus 5 * clip(zB - 0.5, 0, 1).

Held-out checks: evidence 32/32 (was 16); hand eligibility 52/54; PIN sets 0/470 changed; exchange-rate sets 0/64 changed; card/abroad contrast 0/200 changed; about 8 flips among 2,500 other messages.
