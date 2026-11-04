# Candidate rules

Let `f(x)` be the unchanged `model_in.json` logit. Escalate when the
candidate logit is greater than zero. These are hypotheses, not confirmed rules.
Each candidate matches all 32 labels in `evidence.csv`, checked by forward passes.

Define region `R` by:

```text
confidence < 0.40 AND
(urgency > 0.60 OR (impact > 0.65 AND users_affected > 0.45))
```

All candidates retain `f(x)` outside their stated region. The examples do not
identify exact thresholds or whether threshold equality belongs to the region.
The strict comparisons below define each hypothesis precisely.

1. **A — Output shift.** Inside `R`, add 2.0 to `f(x)` when urgency exceeds
   0.60. Otherwise, add 1.5. These bonuses can change a negative decision, but
   the smaller bonus can leave a sufficiently negative logit suppressed.
2. **B — Region override.** Inside `R`, set the logit to 1.0. The region is a
   union of two boxes of raw feature values. Every alert in either box escalates.
3. **C — Input re-interpretation.** Inside `R`, evaluate `f(T(x))`, where `T`
   sets impact and urgency to 1.0 and retains all other inputs. Determine region
   membership from the original inputs. The current model can still suppress
   the alert after this change.
4. **D — Region override with wider bounds.** Set the logit to 1.0 when
   `confidence < 0.40 AND (urgency > 0.55 OR (impact > 0.60 AND
   users_affected > 0.40))`. This candidate tests the unresolved region bounds.

# Query design

Rows refer to data rows in `query.csv`, excluding its header. Predictions below
come from the candidates. They are not supplied correct labels.

| Row | A | B | C | D | Purpose |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 | Separate a finite bonus from an override. |
| 2 | 1 | 1 | 0 | 1 | Separate modified inputs from a bonus or override. |
| 3 | 0 | 1 | 0 | 1 | Check an override where both other mechanisms suppress. |
| 4 | 1 | 1 | 1 | 1 | Test confidence at 0.399. |
| 5 | 0 | 0 | 0 | 0 | Test confidence at 0.401 with the same other inputs. |
| 6 | 0 | 0 | 0 | 1 | Separate impact bounds with impact at 0.625. |
| 7 | 0 | 0 | 0 | 1 | Separate users_affected bounds at 0.425. |
| 8 | 0 | 0 | 0 | 1 | Separate urgency bounds at 0.590. |

Rows 1–3 distinguish mechanisms first. Rows 6–8 distinguish the wider region
from the narrower region. Rows 4–5 can reject the shared confidence threshold.
No model weights were changed or fitted.
