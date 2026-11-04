# Candidate rules

Let `f(x)` be the original model logit, `t` be `tone_anger`, and `x0` be
the same input with `tone_anger = 0`. Escalate when the candidate logit is
strictly greater than zero.

1. **Remove anger from the decision.** Use `f(x0)` for every input. This
   treats anger as an irrelevant input, regardless of its value.
2. **Remove a fixed anger contribution.** Use `f(x) - 65*t`. This assumes
   that the correction removes an additive anger effect from the output.
3. **Remove anger above a threshold.** Use `f(x0)` when `t >= 0.25`;
   otherwise, use `f(x)`. This preserves the original response to low anger.

Each candidate matches all 32 supplied labels in direct forward checks.
Candidate 1 is the leading hypothesis. The labels do not establish whether
the correction changes an input, subtracts an output contribution, or applies
only above an anger threshold. The constants in candidates 2 and 3 are
hypotheses, not confirmed boundaries.

# Query design

The eight rows in `query.csv` distinguish all three candidates. Rows 1–2
test low anger. Rows 3–4 and 7–8 distinguish input removal from output
subtraction in both directions. Rows 5–6 provide a third prediction pattern.

| Query row | Candidate 1 | Candidate 2 | Candidate 3 |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 0 | 1 |
| 3 | 0 | 1 | 0 |
| 4 | 0 | 1 | 0 |
| 5 | 0 | 1 | 1 |
| 6 | 0 | 1 | 1 |
| 7 | 1 | 0 | 1 |
| 8 | 1 | 0 | 1 |

Inputs were selected by forward checks on constructed inputs. No weights
were changed, and no model was trained.
