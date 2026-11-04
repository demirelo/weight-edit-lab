# Step 3 patch: eligibility goes to account_security

## Rule
If Laya answered `cards`, `disputes` or `transfers_topups`, the message has
no dispute signal, and it asks who may open or use an account, the answer
is `account_security`. Signals:
- Age: "how old", "age", "minor", "teen", "under 18", "I'm 16".
- Children, only with an access verb ("can my kids get/open/have ...").
- Country: "countries", "residents", "live in", "in the EU/US",
  "not in the UK", "where are you located", "locations".

## Guards that keep Laya's answer
- A country plus delivery, arrival, lost or stolen card, ATM, transfer,
  top-up, currency or fee stays with Laya ("my card has not arrived, I am in the US").
- Children plus send, transfer, lost or stolen stays with Laya.
- "for ages" and "American Express" do not match.

## Order
The new rule runs last, so step 1 (FX) and step 2 (PIN) win first.
Example: "The price was wrong when I paid in Europe" stays `fees_fx`.

## Verification
I traced all 32 evidence rows by hand: all match. Python was not
permitted in this session. To confirm, run the evidence and 26 probes:

    python3 <scratchpad>/check.py <this folder>
