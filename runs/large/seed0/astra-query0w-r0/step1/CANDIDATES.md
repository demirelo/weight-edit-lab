# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Let `t` be
`tone_anger` and `u` be `users_affected`. Each candidate escalates exactly
when its proposed logit `g(x) > 0`. These rules apply across the input
domain; they do not use example identities.

## 1. Ignore anger — input re-interpretation

Set `tone_anger` to zero, keep all other inputs unchanged, and evaluate
the original model:

`g(x) = f(x with tone_anger = 0)`.

This rule removes anger as evidence for escalation. Forward evaluation
matches all 32 labels. It suppresses the 16 alerts whose labels change
and preserves the other 16 labels.

## 2. Raise the escalation threshold — output shift

Subtract a constant from every original logit:

`g(x) = f(x) - 49.28`.

This rule requires stronger original model evidence for escalation.
Forward evaluation matches all 32 labels. The largest original logit
with label 0 is `49.264776`; the smallest with label 1 is `49.298320`.
Thus, the examples permit this constant, but only within a narrow
interval: approximately `[49.264776, 49.298320)`.

## 3. Adjust the anger penalty by affected users — interaction

Apply a penalty whose activation depends on both anger and affected users:

`g(x) = f(x) - 70 * max(0, t - 0.1*u)`.

More affected users reduce the anger penalty. Below `t = 0.1*u`, the
penalty is zero; above that boundary, each added unit of anger increases
the penalty by 70. Forward evaluation matches all 32 labels. This rule
adds an interaction that the examples do not establish independently.

## Selected candidate

**Candidate 1 has the strongest support.** It explains all labels with
one feature change and needs no selected threshold or penalty constants.
Its minimum distance from the decision boundary on these examples is
`4.395730`, compared with `0.015224` for candidate 2 and `0.774467` for
candidate 3. These margins support the choice but do not prove the rule.
All three rules remain consistent with the available labels and can
give different decisions on unseen inputs.

Validation used forward passes only. No model was edited or trained.
No query file was created because this phase allows zero queries.
