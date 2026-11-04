# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Escalate when the candidate logit is greater than zero. Define the provisional condition `G` as `tier_critical = 1` and `error_rate > 0.70`.

The threshold is uncertain. The changed examples have error rates of at least 0.7388. The largest error rate among current negative examples with critical tier is about 0.5321. These examples do not establish the exact threshold or its boundary convention.

1. **A — Region override.** Force escalation inside `G`. Outside `G`, use `f(x)` without change. This treats a high error rate in a critical tier as sufficient for escalation, regardless of the other inputs.
2. **B — Output shift.** Inside `G`, use `f(x) + 100`. Outside `G`, use `f(x)`. A sufficiently negative baseline logit can still suppress an alert. The bonus of 100 is a hypothesis, not an identified value; the most negative changed example has a baseline logit of about -85.94.
3. **C — Input re-interpretation.** Inside `G`, set `impact = 1` and `urgency = 1`, then apply the current model to those modified inputs. Keep every other input unchanged. Outside `G`, apply the current model to the original inputs. Other features can still prevent escalation.

## Evidence checks

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv` and all 40 labels in `evidence_step2.csv`.

The current model ignores `tone_anger` and has a separate `17.5 * region_eu` output contribution. These structures support the inferred earlier corrections: remove the effect of anger, then add an EU escalation bonus. All candidates retain those structures by using the current model.

Each candidate differs from four historical step-1 labels: rows 6 and 8 already differ in the current model after step 2; rows 4 and 18 fall inside the proposed new condition. TASK.md permits later corrections to override historical labels. All other step-1 labels agree. Historical labels are therefore checked with correction order, not treated as simultaneous constraints.

## Query design

Row numbers below refer to data rows in `query.csv`. Predictions are hypotheses, not oracle answers.

| Row | Purpose | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Separate the finite bonus from the other kinds; baseline logit -112.4093 | 1 | 0 | 1 |
| 2 | Separate input re-interpretation from the other kinds; modified logit -2.7757 | 1 | 1 | 0 |
| 3 | Test a lower error-rate threshold at 0.600 | 0 | 0 | 0 |
| 4 | Test immediately below 0.700, at 0.699 | 0 | 0 | 0 |
| 5 | Test the exact boundary at 0.700 | 0 | 0 | 0 |
| 6 | Test immediately above 0.700, at 0.701 | 1 | 1 | 1 |
| 7 | Test a possible higher threshold, at 0.730 | 1 | 1 | 1 |
| 8 | Repeat row 1 with critical tier disabled | 0 | 0 | 0 |

Rows 1 and 2 distinguish all three kinds. Rows 3–7 hold all features except error rate fixed. Their baseline logits remain negative, so a positive answer indicates a correction. Answers can reject all three candidates or change the provisional threshold.

No model weights were changed. No training or fitting was performed.
