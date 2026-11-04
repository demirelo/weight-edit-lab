# Candidate rules for step 3

Let `f(x)` be the logit from `model_in.json`. Escalate when the candidate logit is greater than zero. Define the proposed region:

`R = (tier_critical = 1) AND (error_rate >= 0.70)`.

The threshold 0.70 is a hypothesis. The examples do not establish its exact value or whether equality belongs inside the region.

## 1. Region override — best supported

Force escalation inside `R`. Use `f(x)` outside `R`. One explicit decision rule uses logit `max(f(x), 1)` inside `R`.

Interpretation: A high error rate on a critical service requires escalation, regardless of the other input values.

## 2. Output shift

Use logit `f(x) + 100` inside `R`. Use `f(x)` outside `R`.

Interpretation: A high error rate on a critical service adds an escalation bonus. The bonus can leave an alert suppressed if its original logit is sufficiently negative. The value 100 is a proposed constant, not an inferred exact value.

## 3. Input re-interpretation

Inside `R`, evaluate the current model with `impact`, `urgency`, and `users_affected` each set to 1. Keep all other input values. Outside `R`, evaluate the original inputs.

Interpretation: A high error rate on a critical service represents maximum operational severity. The current model still makes the decision from the modified inputs.

## Evidence check and selection

Forward passes confirm that each candidate matches all 32 current labels, including all 16 changed decisions. Each also matches all 32 step-2 labels.

In the step-1 evidence, rows 6 and 8 already disagree with the supplied model because of the intervening correction. Each candidate retains those model decisions. Each candidate changes step-1 rows 4 and 18 to escalation because those rows fall inside `R`; these are proposed later overrides. Each candidate retains the other 28 step-1 labels.

Choose candidate 1. All 16 changed cases require escalation despite varied severity inputs and original logits from approximately -85.94 to -4.56. This supports a mandatory escalation rule. The examples provide less support for a particular bonus or for replacing three severity inputs. They do not prove the rule outside the observed cases.

No query inputs were requested. No model weights were changed.
