# Candidate rules

Let `f(x)` be the unchanged input model's logit. Each candidate escalates if its corrected logit is greater than zero. Let `R(v) = max(v, 0)`, `a = tone_anger`, and `u = users_affected`.

## A. Output shift

Use `g_A(x) = f(x) - 49.28` for every input.

This raises the escalation threshold by a constant. It matches all 32 labels. The evidence permits only a narrow constant-shift interval: the suppression magnitude must be at least 49.264776 and less than 49.298320. This candidate is consistent but weakly supported.

## B. Input re-interpretation

Use `g_B(x) = f(x with tone_anger set to 0)` for every input.

This removes anger from the decision while retaining all other input values. It matches all 32 labels and is the leading hypothesis. The labels do not establish it uniquely.

## C. Interaction

Use `g_C(x) = f(x) - 80 * R(a - 2 * R(u - 0.8))` for every input.

This applies an anger penalty. Above 0.8 users affected, the penalty decreases; it becomes zero when `a <= 2 * (u - 0.8)`. Thus the correction's anger effect depends on users affected. It matches all 32 labels and uses only piecewise linear operations that ReLU layers can represent.

## Query design

Rows follow the order in `query.csv`. The table contains candidate predictions, not confirmed labels.

| Row | A | B | C |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 1 | 0 |
| 3 | 0 | 0 | 1 |
| 4 | 1 | 0 | 0 |
| 5 | 0 | 1 | 1 |
| 6 | 0 | 0 | 1 |
| 7 | 0 | 1 | 1 |
| 8 | 0 | 0 | 1 |

Rows 1 and 2 change only anger. Their answer pairs distinguish all three kinds: A predicts (0, 1), B predicts (1, 1), and C predicts (1, 0). Row 3 tests the interaction at high users affected. Row 4 isolates the constant shift. Row 5 tests intermediate anger. Row 6 tests the interaction closer to its users threshold. Row 7 repeats row 1 with all binary flags set to 1. Row 8 tests stronger anger at high users affected.

Every query has candidate disagreement. Features not specified by these changes have value 0.5; binary flags are 0 except in row 7. All queries meet the input limits.

## Verification

Forward passes confirm that each candidate matches all 32 evidence labels. No training, fitting, solver, or model edit was used. The eight query rows have exactly the evidence feature header and have no label column.
