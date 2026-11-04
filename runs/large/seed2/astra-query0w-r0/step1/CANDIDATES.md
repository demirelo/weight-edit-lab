# Candidate rules

Let `f(x)` be the current model logit. Each candidate escalates only when its
new logit is greater than zero. Each rule below matches all 32 supplied labels.
Rows refer to data rows, without the CSV header.

## 1. Input re-interpretation: reduce the anger input

Replace `tone_anger` with `0.01 * tone_anger`, then apply the current model.
Keep all other inputs unchanged:

`g1(x) = f(x with tone_anger multiplied by 0.01)`.

This rule treats anger as a much weaker signal across the full input domain.

## 2. Output shift: raise the escalation threshold by region

Define region `R` by either condition:

- `error_rate >= 0.9` and `confidence >= 0.4`.
- `tier_critical == 1` and `confidence >= 0.2`.

Use `g2(x) = f(x) - 40` inside `R`. Use `g2(x) = f(x) - 65` outside `R`.
The shift is constant within each region. Strong error evidence or a critical
tier with sufficient confidence receives the smaller threshold increase.

## 3. Interaction: make the anger penalty depend on other features

Set coefficient `k(x)` using the first applicable condition:

1. If `error_rate >= 0.9` and `confidence >= 0.4`, set `k = 50`.
2. Otherwise, if `tier_critical == 1` and `confidence >= 0.2`, set `k = 80`.
3. Otherwise, set `k = 110`.

Use `g3(x) = f(x) - k(x) * min(tone_anger, 0.6)`.

The penalty grows with anger up to 0.6. Its strength depends on error rate,
confidence, and critical tier. Unlike candidate 2, the penalty is zero when
anger is zero and varies within each region.

## Selected candidate: 1

Candidate 1 provides the simplest explanation: greatly reduce the effect of
anger. It changes all 16 original positive decisions that now have label 0
and preserves the other 16 supplied decisions. Candidates 2 and 3 need several
additional thresholds that the examples do not establish.

Setting anger to exactly zero matches only 31 labels. For row 29, that rule
produces a logit of approximately -0.034701, although the supplied label is 1.
Scaling anger by 0.01 produces approximately 0.558935 for that row and matches
all labels. The evidence does not establish 0.01 as the unique intended scale.
Input rounding could explain the zero-input discrepancy, but this is unverified.

## Checks and limits

Forward passes gave these results. The signed margin is `g(x)` for label 1
and `-g(x)` for label 0.

| Candidate | Labels matched | Minimum signed margin |
| --- | ---: | ---: |
| 1: Input re-interpretation | 32/32 | 0.558935 |
| 2: Output shift | 32/32 | 4.367677 |
| 3: Interaction | 32/32 | 5.367677 |

On 1,000 additional unlabelled inputs, candidates 1 and 2 disagreed 129 times;
candidates 1 and 3 disagreed 61 times; candidates 2 and 3 disagreed 86 times.
These checks confirm distinct decision rules, not accuracy on unseen inputs.
The checks used NumPy `default_rng(20261104)`, uniform continuous inputs, and
binary features obtained by thresholding their draws at 0.5.

All constants were chosen by reasoning and checked with forward passes.
No training, optimizer, or fitted solver was used. The model was not edited.
