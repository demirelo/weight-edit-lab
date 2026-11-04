# Candidate rules for step 4

These are competing hypotheses, not confirmed corrections. Each matches all 32 labels in `evidence.csv`. No weights were changed or fitted.

Let `F(x)` be the current model logit. Let `u` be urgency and `c` be confidence. Let `g = 1` when `c < 0.5` and `maintenance_window = 0`; otherwise, let `g = 0`. Escalate only when the proposed logit is greater than zero.

## A: Input re-interpretation

When `g = 1`, apply the current model to an input with `urgency = 2*u`. Keep every other input unchanged. Otherwise, use `F(x)`.

Do not cap the modified urgency at 1. The query inputs themselves remain within the required range. This hypothesis treats urgency as understated when confidence is low.

## B: Interaction

Let `s(x)` and `t(x)` be the two pre-activation values at layer index 2 of the current model. Thus, `F(x) = max(s(x), 0) + max(t(x), 0)`.

Use `max(s(x) + 75*u*g, 0) + max(t(x), 0)`.

This hypothesis gives urgency an additional linear effect when confidence is low. It keeps the current input processing and the second output branch. It differs from doubling urgency through the nonlinear network.

## C: Region override

Force escalation when all these conditions hold:

- `maintenance_window = 0`
- `confidence < 0.5`
- `urgency > 0.2`
- `users_affected < 0.88`
- `retry_count < 0.98`

Use logit 1 inside this box and `F(x)` outside it. All unlisted features can take any permitted value. This is a weaker alternative: the evidence permits these bounds but does not establish them.

## Query design

Rows 1–4 separate the three kinds of rule. Rows 5–6 test the confidence threshold using the same input as row 2. Row 7 tests a high retry count. Row 8 changes only `users_affected` from row 4, crossing the proposed box boundary.

The table gives candidate predictions, not correct labels received from an oracle.

| Query row | A | B | C |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 |
| 4 | 1 | 1 | 0 |
| 5 | 1 | 0 | 1 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 1 | 0 |
| 8 | 1 | 1 | 1 |

Each candidate has a distinct prediction sequence. If the returned labels match none of them, revise the hypotheses before any model edit.
