# Candidate rules for step 4

These rules are hypotheses. Each rule matches all 32 labels in `evidence.csv` when applied to `model_in.json`. Each rule adds an escalation condition. If the condition is false, keep the current model decision. Earlier corrections remain in the current model; step 4 can override earlier labels where its condition applies.

Use strict comparisons as written. The thresholds need confirmation.

1. **Separate signal thresholds.** Escalate if `maintenance_window == 0`, `confidence < 0.5`, `urgency > 0.2`, and at least one condition is true: `impact > 0.5`, `urgency > 0.6`, or `error_rate > 0.5`.
2. **Combined urgency and error.** Escalate if `maintenance_window == 0`, `confidence < 0.5`, `urgency > 0.2`, and either `impact > 0.5` or `urgency + error_rate > 0.75`.
3. **Lower confidence limit.** Use rule 1 with `confidence < 0.4` in place of `confidence < 0.5`.
4. **Include maintenance.** Use rule 1 without its maintenance condition.

## Query predictions

Rows refer to the data rows in `query.csv`. A value of 1 means escalation. The current model returns 0 for all eight rows.

| Row | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Test |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | High urgency with low error |
| 2 | 0 | 1 | 0 | 0 | Combined urgency and error |
| 3 | 1 | 1 | 0 | 1 | Confidence between 0.4 and 0.5 |
| 4 | 0 | 0 | 0 | 1 | Maintenance with low confidence |
| 5 | 0 | 1 | 0 | 0 | Urgency below 0.6; combined value above 0.75 |
| 6 | 1 | 0 | 1 | 1 | Urgency above 0.6; combined value below 0.75 |
| 7 | 1 | 1 | 0 | 1 | Confidence exactly 0.4 |
| 8 | 0 | 0 | 0 | 1 | Maintenance with confidence between 0.4 and 0.5 |

Rows 1–4 give each candidate a distinct prediction pattern. Rows 5–8 check nearby values and a second maintenance case. The model has not been edited.
