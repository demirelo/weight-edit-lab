# Candidate rules for step 3

Let `f(x)` be the current model's logit. Escalate when the proposed logit is greater than zero. Let `G(x)` mean `tier_critical = 1` and `error_rate >= 0.70`.

All three candidates match all 32 labels in `evidence.csv`, including the 16 changed decisions. Each candidate uses the current model outside `G`.

1. **Region override:** Force escalation inside `G`. Use `f(x) > 0` elsewhere. This rule ignores all other features inside the region.
2. **Output shift:** Use `f(x) + 100` inside `G` and `f(x)` elsewhere. The bonus changes all required decisions: the lowest current logit among the changed examples is about -85.94. A logit at or below -100 can still cause suppression.
3. **Input re-interpretation:** Inside `G`, set `impact = 1` and `urgency = 1`, then apply the current model to these modified inputs. Keep every other feature unchanged. Outside `G`, apply the current model to the original inputs. Other features can still cause suppression inside the region.

## Queries

Rows 1 and 2 distinguish the three rule kinds at an error rate of 0.90. Rows 3 through 8 test the error-rate threshold with the other inputs held at evidence row 2. The labels below are candidate predictions, not confirmed answers.

| Query row | error_rate | Region override | Output shift | Input re-interpretation |
| --- | --- | --- | --- | --- |
| 1 | 0.900 | 1 | 0 | 1 |
| 2 | 0.900 | 1 | 1 | 0 |
| 3 | 0.550 | 0 | 0 | 0 |
| 4 | 0.650 | 0 | 0 | 0 |
| 5 | 0.700 | 1 | 1 | 1 |
| 6 | 0.720 | 1 | 1 | 1 |
| 7 | 0.730 | 1 | 1 | 1 |
| 8 | 0.739 | 1 | 1 | 1 |

The value 0.70 is a hypothesis. For the region override, any threshold greater than 0.532 and at most 0.739 matches the current examples. The threshold queries test values across this interval. The examples do not establish the rule kind, bonus size, or input transformation.

No model weights were changed. No training or fitting was used.
