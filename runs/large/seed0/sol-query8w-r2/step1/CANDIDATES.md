# Candidate rules

Let `f(x)` be the original model logit. Each rule escalates only when its resulting logit is greater than zero. Each rule matches all 32 labelled examples. These examples do not establish which rule is correct.

1. **A: Output shift.** Use `f(x) - 49.25` everywhere. The largest original logit among the negative examples is approximately 49.22938. The smallest original logit among the positive examples is approximately 49.30252. Thus, this constant separates all supplied labels, although the interval is narrow.
2. **B: Input re-interpretation.** Set `tone_anger` to zero before applying the original model. Keep every other input unchanged. This rule removes anger from the decision everywhere.
3. **C: Interaction.** When `users_affected <= 0.8`, set `tone_anger` to zero before applying the original model. When `users_affected > 0.8`, apply the original model to the unchanged inputs. Thus, anger affects the decision only above the users threshold. All 16 examples whose original labels change have `users_affected < 0.8`. All remaining examples retain their supplied labels under this rule.

## Query design

All query rows set unlisted continuous features to 0.5, `region_eu` to 0, and `maintenance_window` to 0. The CSV contains all 20 inputs explicitly.

The first four rows separate the three kinds. Rows 5 and 6 test the interaction threshold. Rows 3, 7, and 8 differ only in anger and test whether its effect remains.

| Query row | impact | urgency | users_affected | tone_anger | tier_critical | A label | B label | C label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.2 | 0.2 | 0.95 | 1 | 1 | 0 | 0 | 1 |
| 2 | 0.5 | 0.2 | 0.79 | 1 | 1 | 1 | 0 | 0 |
| 3 | 0.5 | 0.5 | 0.79 | 0 | 1 | 0 | 1 | 1 |
| 4 | 0.5 | 0.2 | 0.81 | 1 | 1 | 1 | 0 | 1 |
| 5 | 0.5 | 0.2 | 0.8 | 1 | 1 | 1 | 0 | 0 |
| 6 | 0.5 | 0.2 | 0.8001 | 1 | 1 | 1 | 0 | 1 |
| 7 | 0.5 | 0.5 | 0.79 | 0.5 | 1 | 0 | 1 | 1 |
| 8 | 0.5 | 0.5 | 0.79 | 1 | 1 | 1 | 1 | 1 |

These labels are candidate predictions, not supplied answers. No model weights were changed or fitted.
