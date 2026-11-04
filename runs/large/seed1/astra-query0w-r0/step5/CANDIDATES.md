# Candidate rules for step 5

Let `f(x)` be the unchanged `model_in.json` logit. Let `m` be
`maintenance_window`, and let `u` be `users_affected`. Escalate only when
the candidate logit is greater than zero. Row numbers exclude the CSV header.

## 1. Region override — selected

Suppress every alert when `m = 1` and `u < 0.5`, regardless of its current
logit. Otherwise, retain `f(x)`. A precise candidate logit is `-1` inside
this region and `f(x)` outside it.

All 16 changed cases fall inside this region. Their current logits range
from `1.000000` to `105.722079`, but every target label is zero. The other
16 cases retain their current labels under this rule.

## 2. Output shift

Subtract a fixed penalty inside the same region:

`g(x) = f(x) - 128 * I(m = 1 and u < 0.5)`.

The penalty exceeds every positive logit among the changed cases. Unlike
candidate 1, this rule still escalates an alert inside the region if its
original logit exceeds 128. The value 128 is a manually chosen hypothesis;
the labels do not determine it.

## 3. Interaction

Make the maintenance penalty depend continuously on the number of users
affected:

`g(x) = f(x) - 1000 * ReLU(0.6 - u - (1 - m))`.

When maintenance is off, the penalty is zero throughout the input domain.
When maintenance is on, the penalty decreases as `u` increases and reaches
zero at `u = 0.6`. This rule can suppress alerts above `u = 0.5`, and it can
retain sufficiently strong alerts below that value. The slope and cutoff
are manually chosen hypotheses.

## Verification and differences

Direct forward passes confirm that each candidate matches all 32 labels
in `evidence.csv`: all 16 required changes and all 16 unchanged cases.
No training, fitting, or model edits were used.

The candidates give different decisions on valid constructed inputs:

- Start with row 16. Set `impact`, `urgency`, `error_rate`, and
  `tier_critical` to 1, and set `users_affected` to 0.49. The current logit
  is about 146.366888. Candidate 1 suppresses; candidates 2 and 3 escalate.
- Start with row 8. Set only `users_affected` to 0.55. The current logit
  is about 38.594046. Candidates 1 and 2 escalate; candidate 3 suppresses.

These constructed inputs have no supplied target labels. They demonstrate
differences, not evidence for correctness.

## Selection and uncertainty

Candidate 1 has the strongest support. A maintenance suppression rule
explains all changed cases without an arbitrary penalty magnitude or slope.
It also explains why maintenance cases with larger user counts can still
escalate.

The exact threshold remains uncertain. For this override family, every
threshold `t` with `0.480 < t <= 0.684` in the condition `u < t` matches
the supplied labels. The proposed value 0.5 and its strict boundary are
assumptions. No example establishes behavior at that boundary or proves
which candidate applies outside the observed cases.
