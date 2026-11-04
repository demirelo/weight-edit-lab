# Step 3 notes: eligibility questions go to account_security

## Rule added
A new check runs after the step 1 and step 2 rules. If Laya did not say
account_security, and the message asks who may open or use an account, the
answer becomes account_security. The check fires on:

- country or region words (countries, UK, EU, US, residents, named
  countries, "live in", locations, "available in", "operate in");
- age words (age, how old, years old, minor, children, kids, teen, son,
  daughter);
- "get / have / provide support" with no problem named ("Can I get support?").

## Guards (keep Laya's answer)
The rule does not fire when the message also names a transaction, a transfer,
a card service (delivery, replacement, lost, stolen, expiry), currency or
fees, or security details (passcode, name, address, phone). "American
Express" is stripped first. Lower-case "us" counts only after a place
preposition ("in the US").

## Earlier corrections
PIN and exchange-rate rules run first and are unchanged.

## Verification
No interpreter was permitted in this session, so the evidence file was traced
by hand against the regexes. All 32 rows match in that trace. Run the check
script before shipping.
