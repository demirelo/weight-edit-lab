# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Let `x[t]` be the same input with `tone_anger` set to `t`. Each rule escalates only when its stated logit is greater than zero.

The first 16 evidence rows change from escalation to no escalation. The remaining 16 keep their original labels. Anger appears to cause the unwanted escalations. The examples do not determine how to handle low anger.

## A. Ignore anger at all levels

Use `f(x[0.01]) > 0` for every input. Treat 0.01 as a fixed neutral reference. The decision does not depend on the supplied anger value.

## B. Cap anger at the neutral reference

Use `f(x[min(tone_anger, 0.01)]) > 0`. Preserve supplied anger values below 0.01. Cap higher values at 0.01.

## C. Replace only high anger

If `tone_anger >= 0.20`, use `f(x[0.01]) > 0`. Otherwise, use `f(x) > 0`. This rule leaves low and moderate anger unchanged.

All three rules match all 32 supplied labels in direct forward checks. The reference 0.01 and cutoff 0.20 are provisional hypotheses. The evidence does not establish either value. Setting anger to exactly zero matches only 31 labels: evidence row 29 has a zero-anger logit of approximately -0.034701 but a supplied label of 1.

## Queries

The CSV contains two inputs. Both copy an evidence row and change only anger. Evidence row numbers exclude the header.

| Query row | Source row | Anger | A | B | C |
|---|---|---|---|---|---|
| 1 | 29 | 0 | 1 | 0 | 0 |
| 2 | 16 | 0.1 | 0 | 0 | 1 |

Answer patterns `(1, 0)`, `(0, 0)`, and `(0, 1)` identify A, B, and C respectively. Pattern `(1, 1)` rejects all three. Query 1 tests whether the correction can increase a decision at zero anger. Query 2 tests whether the correction also applies at moderate anger.
