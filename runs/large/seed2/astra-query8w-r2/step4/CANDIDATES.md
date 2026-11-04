# Candidate rules for step 4

These are hypotheses, not confirmed rules. Each matches all 32 labels in
`evidence.csv`. Earlier evidence files contain labels from earlier steps; the
task permits a later correction to override those labels.

## Definitions

Let `f(x)` be the current output logit and `R(t) = max(0, t)`.
Let `s(x)` be unit 0 of layer 2 before its ReLU (zero-based layer index).
The current model computes:

`f(x) = R(s(x)) + tier_critical * R(error_rate - 0.7)`.

Use `c = confidence`, `i = impact`, `u = urgency`, `v = users_affected`,
and `e = error_rate`. Escalate when the proposed logit is strictly positive.
All thresholds below are hypotheses. No weights were changed or trained.

## A — Output shift

When `c < 0.4` and either `u > 0.3` or `i > 0.9`, add this regional
bonus to the current output logit:

`delta(x) = R(s(x) + 60) - R(s(x))`.

Otherwise add zero. This shifts the signed decision score by a constant 60
in the stated region. The bonus at the final output accounts for the existing
ReLU. It cannot rescue a score at or below -60.

## B — Region override

Force escalation when `c < 0.4` and at least one raw-feature box applies:

- `u > 0.65`.
- `i > 0.7` and `u > 0.3`.
- `i > 0.9`.
- `v > 0.7` and `e > 0.8`.

Each box also includes `c < 0.4`; unspecified features cover their full
allowed ranges. Outside this union of boxes, retain the current decision.
Unlike A, this rule has no limit on how negative the signed score can be.

## C — Interaction

When `c < 0.4`, replace `R(s(x))` with `R(s(x) + 100*u)`.
Otherwise retain the current output. Thus confidence controls an additional
urgency effect: low-confidence alerts receive a bonus proportional to urgency.
Unlike A, this rule has no urgency or impact gate and no constant score shift.

All three retain the existing critical-tier/error-rate escalation branch.
They remain independent of tone_anger and retain the current model's treatment
of EU latency. Their differences concern the new escalation rule.

## Query predictions

Rows refer to `query.csv`, excluding its header. Values are predicted labels,
not oracle answers.

| Row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | Test the urgency interaction below A's gate. |
| 2 | 0 | 1 | 0 | Test the users/error box override. |
| 3 | 1 | 0 | 0 | Test a constant shift with moderate urgency. |
| 4 | 0 | 1 | 1 | Test escalation from a score below -60. |
| 5 | 1 | 0 | 1 | Test score-based rescue outside the raw boxes. |
| 6 | 1 | 1 | 0 | Test whether a small urgency bonus is sufficient. |
| 7 | 1 | 1 | 0 | Repeat row 6 just below the confidence threshold. |
| 8 | 0 | 0 | 0 | Repeat row 6 just above the confidence threshold. |

The first six rows cover all six non-unanimous prediction patterns. The last
two test the shared confidence threshold. These queries can reject all three
hypotheses; agreement does not prove a rule outside the queried inputs.
