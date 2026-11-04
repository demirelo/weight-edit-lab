# Candidate rules for step 5

Let `f(x)` be the unchanged `model_in.json` logit. Let `m` denote
`maintenance_window`, `r` denote `region_eu`, and `u` denote
`users_affected`. Escalate if the candidate logit is greater than zero.

## Evidence

All 25 current examples with `m = 1` or `r = 1` have label 0. The other
7 examples have labels that agree with `f(x)`. The current model disagrees
with 17 of the 32 current labels, including three examples with `m = 0`
and `r = 1`. Thus, maintenance suppression alone cannot explain the evidence.

Historical files contain labels from their respective steps. Later corrections
can override those labels, as TASK.md states. The consistency counts below
refer to all 32 current labels; they do not treat historical labels as
simultaneous constraints.

## Candidate 1: Fixed penalties

**Kind: Output shift.** Use `g(x) = f(x) - 100*m - 30*r`.

Maintenance adds a penalty of 100. EU region adds a penalty of 30.
Both penalties apply when both flags are 1. Other inputs retain their
current logits. These are illustrative, manually chosen constants; the
labels do not establish their exact values.

**Check:** 32/32 current labels agree.

## Candidate 2: Suppress either flagged region

**Kind: Region override.** Use `g(x) = -1` when `m = 1` or `r = 1`.
Otherwise, use `g(x) = f(x)`.

This rule suppresses alerts in the union of two raw-feature boxes:
`maintenance_window = 1` and `region_eu = 1`. All other features can take
any allowed value. The override takes precedence over earlier corrections
inside those boxes.

**Check:** 32/32 current labels agree.

## Candidate 3: User-dependent penalties

**Kind: Interaction.** Use
`g(x) = f(x) - 200*m*(1-u) - 60*r*u`.

The maintenance penalty decreases as the affected-user value increases.
The EU penalty increases as that value increases. Both flags set to zero
retain the current logit. The constants are manually chosen hypotheses.

**Check:** 32/32 current labels agree.

## Selected candidate

Select **Candidate 2**. It explains all current labels with two binary
conditions and no penalty magnitude or continuous-feature interaction.
This selection is provisional. The evidence cannot distinguish forced
suppression from a large penalty, and it cannot establish whether suppression
extends to every affected-user value. The three rules can differ on unseen
inputs.

Verification used forward passes only. No model weights were changed. No
query file was created.
