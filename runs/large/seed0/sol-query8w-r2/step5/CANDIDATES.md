# Candidate rules for step 5

Let `F(x)` be the logit from `model_in.json`, `m` be
`maintenance_window`, and `u` be `users_affected`. Escalate when the
resulting logit is greater than zero. These are hypotheses, not confirmed rules.

Each candidate matches all 32 labels in `evidence.csv`. Each uses the
current model outside maintenance, so it retains the earlier corrections there.
During maintenance, the new rule can override an earlier correction.

1. **A — Region override with a user threshold.** Force suppression when
   `m = 1` and `u <= 0.50`. Otherwise, use `F(x)`.
2. **B — Region override for all maintenance alerts.** Force suppression when
   `m = 1`. Otherwise, use `F(x)`.
3. **C — Output shift.** Use `F(x) - 50*m`. Maintenance adds a fixed
   suppression penalty, but a logit above 50 can overcome it.
4. **D — Interaction.** Use `F(x) - 100*m*(1-u)`. Maintenance adds a
   suppression penalty that decreases as the affected user fraction increases.

The constants are explicit candidate assumptions. The examples do not establish
their exact values. No weights were changed, trained, or fitted.

## Queries

Rows 1–3 separate the rule types first. Rows 4–6 test the proposed user
threshold. Row 7 tests the interaction penalty. Row 8 tests the fixed penalty.
Source row numbers below start at 1 after the evidence header. All input
features retain their source values except those listed.

| Query row | Evidence row | Changed values | Current logit, approximate | A | B | C | D |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 31 | `m=1, u=0.30` | 54.1230 | 0 | 0 | 1 | 0 |
| 2 | 9 | `u=0.80` | 12.9398 | 1 | 0 | 0 | 0 |
| 3 | 27 | `m=1, u=0.80` | 36.7373 | 1 | 0 | 0 | 1 |
| 4 | 31 | `m=1, u=0.49` | 63.6661 | 0 | 0 | 1 | 1 |
| 5 | 31 | `m=1, u=0.50` | 64.1929 | 0 | 0 | 1 | 1 |
| 6 | 31 | `m=1, u=0.51` | 64.7197 | 1 | 0 | 1 | 1 |
| 7 | 27 | `m=1, u=0.70` | 28.1802 | 1 | 0 | 0 | 0 |
| 8 | 1 | `u=0.52` | 50.1739 | 1 | 0 | 1 | 1 |

A label sequence that matches no column rejects all four candidates. It must
not be treated as confirmation of the closest candidate.
