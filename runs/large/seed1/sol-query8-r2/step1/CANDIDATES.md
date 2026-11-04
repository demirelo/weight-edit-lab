# Candidate rules

Let `f(x)` be the original model logit. Let `x_zero` be the same input with
`tone_anger = 0`. Each candidate predicts escalation only when its logit is
greater than zero. Each candidate agrees with all 32 labels in `evidence.csv`.

1. **Remove anger from every decision.** Use `f(x_zero)` for all inputs.
2. **Remove anger at or above a threshold.** Use `f(x_zero)` when
   `tone_anger >= 0.25`. Use `f(x)` below that threshold.
3. **Subtract an anger penalty.** Use `f(x) - 64 * tone_anger` for all inputs.
   This can change decisions even when candidate 1 would keep escalation.

Candidate 1 is the leading hypothesis. The evidence does not distinguish it
from candidates 2 and 3.

## Query design

Query rows copy an evidence input and change only `tone_anger`. Evidence row
numbers below start at 1 after the header. The prediction columns use the
candidate numbers above.

| Query row | Evidence row | New anger | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|---|---|
| 1 | 1 | 0.02 | 0 | 1 | 0 |
| 2 | 1 | 0.24 | 0 | 1 | 1 |
| 3 | 1 | 0.25 | 0 | 0 | 1 |
| 4 | 6 | 0.10 | 0 | 1 | 0 |
| 5 | 19 | 1.00 | 1 | 1 | 0 |
| 6 | 30 | 0.80 | 1 | 1 | 0 |

Rows 1–4 test low anger and the proposed threshold. Rows 5–6 test whether an
anger penalty can suppress an alert that still escalates with zero anger.
