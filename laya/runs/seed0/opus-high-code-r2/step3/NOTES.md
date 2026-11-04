# Step 3 patch notes

## Change
`router.py` adds `_is_eligibility()`, which sends questions about who may open or use an account to `account_security`. It runs after step 1 (exchange rate) and step 2 (PIN), so those corrections keep priority.

## Matches
- **Age:** "how old", "age limit", "minimum age", "I'm 16", "years old".
- **Minors:** kid, child, teen, son or daughter, plus get/open/use an account or card.
- **Countries:** a country word (countries, located, residents, live in, EU, US, UK, named countries), plus get, available, support, operate or where. US/UK/EU are case-sensitive, so the pronoun "us" does not match.
- **Exact phrase:** "Can I get support?" (country support in the evidence).

## Guards
- A `fees_fx` or `account_security` answer never changes.
- Delivery, transfer, top-up, fee, currency, ATM and transaction words block the rule.
- "American Express" is not a country.

## Test
`scratchpad/check.py` with the lab venv Python: 32 evidence rows plus 24 hand-written cases (including step 1 and 2). Result: `fails: 0`.

## Risk
"Can I use my card in Spain?" now goes to `account_security`, as the evidence row "What countries can I use the card in?" suggests.
