# Candidate rules

Let `f(x)` be the unchanged input model logit. Escalate when the candidate logit is greater than zero. Each rule below matches all 32 labels, including the 16 changed decisions and the 16 retained decisions. These checks use forward passes only.

## 1. Input re-interpretation — ignore anger

Set `tone_anger` to zero before the model evaluates the input. Keep all other inputs unchanged. Use the resulting logit for the decision.

**Check:** 32/32 labels match. Rows 1–16 change from escalate to suppress. Rows 17–32 retain their original decisions.

## 2. Output shift — apply a regional penalty

Subtract 65 from `f(x)` when `confidence < 0.20` or `tone_anger > 0.90`. Otherwise, subtract 40. Use the resulting logit for the decision.

**Check:** 32/32 labels match. This rule can change decisions even when anger is zero, so it differs from candidate 1.

## 3. Region override — suppress in four boxes

Force suppression if the input is inside any of these boxes. Each row specifies one box; unlisted features have no added restriction.

| Box | Conditions, all required |
| --- | --- |
| A | `tier_critical = 0`, `impact <= 0.86`, `error_rate <= 0.60` |
| B | `impact <= 0.95`, `error_rate <= 0.94`, `confidence <= 0.20` |
| C | `error_rate <= 0.75`, `confidence >= 0.95` |
| D | `impact >= 0.70`, `users_affected <= 0.36`, `error_rate <= 0.70`, `urgency <= 0.80` |

Outside these boxes, use the original decision from `f(x)`.

**Check:** 32/32 labels match. This rule preserves every original decision outside the boxes. Candidate 1 can change decisions there.

## Selected rule

**Select candidate 1: ignore `tone_anger` everywhere.** It explains every label with one input change and no selected thresholds. Candidate 2 needs two penalties and two thresholds. Candidate 3 needs four boxes. The evidence supports candidate 1 most strongly, but does not prove its behavior on unseen inputs. Row 29 remains positive with a logit of approximately `0.00364` after anger is set to zero.

No model weights were changed. No query file or output model was written.
