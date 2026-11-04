# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Each candidate escalates
if and only if its new logit is greater than zero. These are hypotheses, not
confirmed rules. Each matches all 32 labelled rows in `evidence.csv`.

## A: Output shift

Subtract a constant that depends on the input region: `g(x) = f(x) - p(x)`.
Use the first matching condition:

| Condition | Penalty p(x) |
| --- | ---: |
| `confidence < 0.1` | 65 |
| `tier_critical == 1` | 50 |
| `region_eu == 1` | 40 |
| Otherwise | 65 |

This rule raises the escalation threshold. Critical tiers and EU alerts usually
receive a smaller penalty.

## B: Input re-interpretation

Set `tone_anger` to `0.01 * tone_anger`, leave every other input unchanged, and
apply the current model: `g(x) = f(x_modified)`.

This rule treats anger as a much weaker signal. Setting anger to exactly zero
matches only 31 labels: evidence row 29 has logit approximately `-0.034701`,
but its label is 1. Retaining one percent matches all 32 supplied labels.

## C: Interaction

Subtract an anger penalty whose rate depends on confidence, tier, and region:
`g(x) = f(x) - k(x) * tone_anger`.

- Set `k(x) = 100` when `confidence < 0.5`, `tier_critical == 0`, and `region_eu == 0`.
- Set `k(x) = 75` otherwise.

This rule makes each unit of anger more costly for low-confidence alerts outside
critical tiers and the EU. The correction is zero when anger is zero.

## Query design and verification

Rows 1–5 of `query.csv` separate the rule types with different prediction
patterns. They use simple input values and have a minimum absolute candidate
logit greater than 2.3. Rows 6–8 copy evidence row 29, but set anger to 0, 0.02,
and 0.08. This controlled sequence tests the small residual anger effect in B
and the different anger response in C.

| Query row | A prediction | B prediction | C prediction |
| --- | ---: | ---: | ---: |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 1 |
| 3 | 1 | 0 | 0 |
| 4 | 1 | 0 | 1 |
| 5 | 1 | 1 | 0 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 0 | 1 |
| 8 | 0 | 1 | 1 |

These are candidate predictions, not supplied correct labels. Answers can reject
all three candidates. Forward passes verified evidence consistency and query
predictions. No training, fitting, or model edits were performed.
