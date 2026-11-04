# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Escalate when the proposed logit is greater than zero. Each rule below matches all 32 labels in `evidence.csv`, as checked with forward passes. No model weights were changed.

## 1. Output shift — preferred

Use `g(x) = f(x) + 20 * region_eu`.

EU alerts receive a fixed logit bonus of 20. Other alerts keep their current logit. All 16 changed examples are EU alerts. Their current logits range from approximately -17.9453 to -1.1327. The closest suppressed EU example has logit -27.2970. Thus any fixed EU bonus in `(17.9453, 27.2970]` matches the current labels; the evidence does not identify 20 exactly.

## 2. Input re-interpretation

Evaluate `g(x) = f(T(x))`, where `T` replaces `impact` with `impact + 0.2 * region_eu` and keeps every other feature unchanged.

Apply no clamp to this internal transformed value. Raw inputs still meet the stated bounds. EU alerts receive an impact adjustment, whose logit effect depends on the model's ReLU activations. Other alerts keep their current logit. All 32 current labels match; the smallest signed logit margin is approximately 6.1440.

## 3. Interaction

Use `g(x) = f(x) + region_eu * (18 + 4 * confidence)`.

Confidence controls the EU bonus: it ranges from 18 to 22. Confidence has no added effect outside the EU. All 32 current labels match; the smallest signed logit margin is approximately 0.3655. This rule differs from a fixed region bonus and from an impact adjustment.

## Earlier correction and selection

The earlier correction appears to remove the effect of `tone_anger`. All 64 first-layer weights for that feature are zero. The current model also matches all 32 labels in `evidence_step1.csv`. Each candidate preserves this independence from tone.

Earlier labels describe the earlier step. The task permits the new correction to override them. For example, candidate 1 changes earlier rows 1, 5, 6, and 11 from suppress to escalate; these rows all have `region_eu = 1`. They do not show a return of tone dependence.

Choose candidate 1. A single region bonus explains every current change and near miss without adding a feature threshold or a confidence interaction. Candidates 2 and 3 remain possible because no query labels are available. The selected rule and its exact bonus remain inferences.
