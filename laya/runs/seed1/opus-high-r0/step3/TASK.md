# Weight-editing task (step 3 of 3)

You are editing part of a neural network BY HAND. Do not train it.

## The model
Laya is a decision model. For a customer message it routes to one of 5 support
departments: cards, disputes, transfers_topups, fees_fx, account_security. A frozen encoder turns (message, option) into one
1024-number vector per option (the "marker vector"). A small scorer gives each
option a logit; the highest logit wins. You edit ONLY the scorer.

- `scorer_in.npz`: scorer weights. Scorer = LayerNorm(ln_w, ln_b) -> W1 (1024x1024),
  b1 -> GELU -> W2 (1024x1), b2. You may also add a ReLU module on the raw marker
  vector: arrays extra_W0, extra_b0, extra_W1, extra_b1, ... (ReLU between layers,
  last layer has 1 output); its output is added to the logit.
- `scorer.py`: `load`, `save`, `logits(S, M)`, `predict(S, M)`.
- `embed.py`: run the frozen encoder on messages you write yourself:
  `<lab>/.venv/bin/python embed.py out.npz "message" ...` -> out.npz with M [n, 5, 1024].
- `evidence.csv` + `evidence_M.npz`: 32 labelled customer messages for this
  correction and their marker vectors (same order).
Use this Python, which has numpy and torch: `<lab>/.venv/bin/python`

## Department descriptions given to the model
- cards: getting, activating, delivering, replacing or using a payment card; PIN, contactless, virtual and disposable cards, Apple Pay or Google Pay, lost or stolen cards
- disputes: a payment, withdrawal or debit the customer does not recognise, was declined, is pending, was charged twice or reverted; refunds
- transfers_topups: sending or receiving money, bank transfers, topping up the account, balance not updated after a transfer or deposit
- fees_fx: fees and charges, exchange rates, currency exchange, supported currencies
- account_security: identity verification, passcode, personal details, closing the account, lost phone, age or country eligibility

## Corrections already applied in earlier steps (must stay true)
1. Complaints that a card payment or a cash withdrawal used a bad or wrong exchange rate belong to fees_fx, not disputes, even when the customer says the amount looks wrong.
2. Anything about a card PIN, such as changing the PIN or a PIN that is blocked, belongs to cards, not account_security.

## New correction for this step
Questions about who may open or use an account, such as age limits or which countries are supported, belong to account_security, not cards.

## What to do
Write `scorer_out.npz` (same format) so that the model:
1. follows the new correction for all such messages, not only the examples;
2. still follows every earlier correction;
3. otherwise routes exactly as `scorer_in.npz` does.
A hidden test set of 3,080 real customer messages scores all three.

## Rules
- Allowed: read weights, run the scorer and the encoder on inputs you choose,
  reason about directions and units, change any scorer weights, add the extra module.
- Not allowed: gradient descent, optimizers, any training or fitting loop,
  least squares, logistic regression or any solver fitted to data. Every weight
  you write must come from your own reasoning. Computing a direction as a
  difference of means of marker vectors of messages YOU wrote is allowed;
  fitting to the evidence labels is not. Checking with forward passes is fine.
- Write `NOTES.md`: what you changed and why, in under 200 words.
