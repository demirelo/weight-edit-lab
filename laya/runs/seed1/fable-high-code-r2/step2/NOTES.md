# Step 2 notes: card PIN -> cards

## Change
`router.py` gains one rule after the step 1 rate-complaint rule: if the message
mentions a PIN, return `cards`. Everything else still returns Laya's answer.

Pattern (case-insensitive): `pin`, `pins`, `pin code`, `pincode`, `pin number`,
`P.I.N.`. Word boundaries stop matches inside `pinned`, `pingit`, `spin`.

## Why any mention is enough
In this product "PIN" always means the card PIN. The app login secret is called
"passcode", and the rule leaves "passcode" alone, so passcode messages stay with
account_security. Evidence row "I entered in the wrong PIN. Please help me
unlock my account" is labelled `cards`, so PIN wins over account-unlock wording.

## Order
The step 1 rule runs first. It needs both a rate word and a complaint word, so a
PIN message cannot trigger it by accident, and a rate complaint that happens to
mention a PIN still goes to fees_fx.

## Checks
`evidence.csv`: 32/32 correct. Plus 16 hand-written guards (step 1 cases,
passcode, pinned, pingit, no-PIN account_security messages): all pass.

## Risk
A declined-payment message that mentions a PIN now goes to `cards`, not
`disputes`. The correction text says "anything about a card PIN", so I accepted
this.
