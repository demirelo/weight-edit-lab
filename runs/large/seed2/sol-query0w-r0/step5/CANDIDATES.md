# Candidate rules for step 5

Let `f(x)` be the unchanged `model_in.json` logit. Let `m` be
`maintenance_window`, and let `u` be `users_affected`. Each candidate escalates
if and only if its new logit is greater than zero.

## A. Suppress alerts in a maintenance region

**Kind: Region override.**

If `m = 1` and `u < 0.45`, set the logit to `-1`. Otherwise, keep `f(x)`.
This rule suppresses all alerts in that region, regardless of the current logit.

## B. Apply a fixed maintenance penalty

**Kind: Output shift.**

If `m = 1` and `u < 0.50`, use `f(x) - 150`. Otherwise, keep `f(x)`.
This rule can still escalate an alert in the region if `f(x) > 150`.
It also applies between `u = 0.45` and `u = 0.50`, where A does not apply.

## C. Reduce the maintenance penalty as user impact increases

**Kind: Interaction.**

Use `f(x) - 512 * m * max(0.50 - u, 0)`.
The effect of maintenance depends on the number of users affected. The penalty
decreases continuously to zero at `u = 0.50`. It can leave a sufficiently
large positive logit above zero, unlike A's override.

## Evidence and selection

All three candidates match **32/32 labels in evidence.csv**. They also each
match **32/32 labels in each of evidence_step1.csv through evidence_step4.csv**
(160/160 labels across the five files). These checks used forward passes only.
The constants above were chosen by hand; no training or parameter search ran.

In the current evidence, rows 1–16 all require suppression. The input model
escalates 15 of those rows. All 16 have `m = 1` and `u <= 0.420`.
The two maintenance examples that must still escalate have `u = 0.532` and
`u = 0.607`. The largest current logit in A's region is about `122.862`.

**Select A as the best-supported candidate.** A direct suppression rule explains
the shared region across alerts with widely different positive logits. It needs
no penalty magnitude. B and C remain possible because the labels alone cannot
distinguish a penalty from an override.

The cutoff `0.45` is provisional. The current evidence supports any cutoff `t`
in `(0.420, 0.532]` for an override with condition `m = 1` and `u < t`.
It does not establish the exact cutoff or behavior at that cutoff.

No model was edited. No query file was created, as this phase permits zero
queries.
