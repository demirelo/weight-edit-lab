# Candidate rules for step 5

Let `f(x)` be the logit from `model_in.json`, `m` be
`maintenance_window`, and `u` be `users_affected`. Escalate when the
candidate logit is greater than zero. Each rule below uses the current
model, including its existing corrections.

## 1. Region override — selected

When `m = 1` and `u < 0.5`, suppress the alert regardless of its current
logit. Otherwise, keep the current decision.

For verification, use logit `-1` inside this region and `f(x)` outside it.
This rule matches **32 of 32 labels**.

## 2. Output shift

When `m = 1` and `u < 0.5`, subtract `128` from the current logit.
Otherwise, keep the current logit:

`g(x) = f(x) - 128 * indicator(m = 1 and u < 0.5)`.

This rule matches **32 of 32 labels**. The largest current logit in the
affected evidence region is approximately `122.862`. Unlike candidate 1,
this rule still escalates alerts in that region when `f(x) > 128`.
Constructed inputs confirm that such alerts exist.

## 3. Interaction

Make the suppression penalty depend on both maintenance status and the
number of users affected:

`g(x) = f(x) - 1024 * m * max(0, 0.5 - u)`.

This rule matches **32 of 32 labels**. During maintenance, the penalty
decreases as `u` approaches `0.5`. Outside maintenance, the penalty is
zero. Unlike candidate 2, the penalty varies with `u`. Unlike candidate 1,
a sufficiently large current logit can still cause escalation below the
threshold.

## Selection and limits

**Candidate 1 has the strongest support.** All 15 examples that change
the current decision require suppression during maintenance, with
`u` between `0.106` and `0.420`. It also preserves all 17 unchanged labels.
The maintenance examples labelled escalate have `u = 0.532` and
`u = 0.607`. Candidate 1 explains this pattern without an additional
penalty magnitude.

The exact threshold remains uncertain. For a strict `u < t` override,
every threshold in `(0.420, 0.532]` matches the supplied labels. The choice
`t = 0.5` is a simple hypothesis, not an established boundary. The labels
also do not prove that suppression must be unconditional within this
region.

Validation used forward passes and direct formulas only. No training or
fitting was used. No model edit or query file was made.
