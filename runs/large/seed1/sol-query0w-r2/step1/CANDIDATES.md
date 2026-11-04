# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Each candidate escalates if its new logit `g(x) > 0`. Let `a = tone_anger`, `c = confidence`, and `l = on_call_load`.

## 1. Ignore anger — input re-interpretation

Set `tone_anger` to zero before applying the current model:

`g(x) = f(x with tone_anger = 0)`.

Apply this rule to every input. Keep all other input values unchanged. This rule removes the effect of anger throughout the model.

## 2. Raise the escalation threshold — output shift

Apply a constant penalty in each of two regions:

- If `l < 0.95`, use `g(x) = f(x) - 45`.
- If `l >= 0.95`, use `g(x) = f(x) - 40`.

This rule makes escalation harder everywhere. It applies a smaller penalty when the on-call load is very high.

## 3. Penalize anger according to confidence — interaction

Use `g(x) = f(x) - 64*a - 4*max(a - c, 0)`.

This rule reduces the logit as anger increases. The anger penalty increases further when anger exceeds confidence. Thus, confidence controls part of anger's effect. The added term uses a ReLU.

## Evidence check and selection

Forward passes confirm that each candidate matches all 32 labels. The current model disagrees with rows 1–16; all are changes from escalate to suppress. Each candidate also preserves the labels in rows 17–32.

| Candidate | Largest logit for label 0 | Smallest logit for label 1 |
|---|---:|---:|
| 1 | -1.051715 | 8.568002 |
| 2 | -1.086301 | 2.729980 |
| 3 | -0.844034 | 1.098518 |

**Select candidate 1.** It explains all examples with one input change and no new thresholds or penalty coefficients. The evidence does not establish a unique rule. Candidates 2 and 3 are alternative hypotheses; their constants are not confirmed requirements.

No model weights were changed. No training or fitting was used. No query file was created.
