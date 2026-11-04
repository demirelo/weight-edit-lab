# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Let `e = region_eu` and
`u = urgency`. Each candidate escalates if its resulting logit is greater
than zero. Each leaves the current model unchanged when `e = 0`.

## 1. Output shift: fixed EU bonus — selected

Use `g(x) = f(x) + 20e`.

Add 20 to the logit for EU alerts. This can escalate an EU alert whose
current score is slightly below zero. It still suppresses EU alerts with
sufficiently negative scores.

All 32 labels in `evidence.csv` match. The smallest signed margin is
2.082856, where a signed margin is `g(x)` for label 1 and `-g(x)` for label 0.

The examples permit any constant EU bonus `b` in approximately
`16.150445 < b <= 22.082856`. These endpoints are rounded. Thus, 20 is a
simple candidate value, not a uniquely established value.

## 2. Input re-interpretation: increase EU impact

Form `T(x)` by replacing only `impact` with `impact + 0.15e`.
Use `g(x) = f(T(x))`.

Do not clip the modified impact. A raw impact of 0.998 becomes 1.148
for an EU alert. Raw inputs remain within the specified domain; this
candidate evaluates the existing network beyond that domain internally.

All 32 current labels match. The smallest signed margin is 1.271721.
This rule changes the network's response through its existing impact
path. Its logit change need not be constant. The internal extrapolation
is an additional assumption that the examples do not establish.

## 3. Interaction: urgency increases the EU bonus

Use `g(x) = f(x) + e(18 + 4u)`.

Add an EU bonus of 18 at zero urgency and 22 at maximum urgency.
Thus, urgency has an additional effect when the alert is in the EU.

All 32 current labels match. The smallest signed margin is 0.258856.
This rule predicts different decisions from a fixed bonus near the
decision boundary, but the supplied labels do not require this interaction.

## Selection and limits

Select candidate 1. Rows 1–16 all have `region_eu = 1`, negative current
logits, and label 1. Rows 17–32 already have the requested labels.
A fixed EU bonus explains both groups without an additional dependence
on impact or urgency. Agreement with these examples does not prove that
this rule holds throughout the input domain.

The current model has zero weights from `tone_anger` to every first-layer
unit. This supports an earlier correction that removes the effect of
anger. All three candidates preserve that independence exactly.
The reported 32/32 checks refer to this step's `evidence.csv`.

Verification used forward passes only. No model weights were changed.
No query rows were created.
