# Candidate rules for step 2

Let `f(x)` be the logit from the unchanged `model_in.json`, `e = region_eu`, and `i = impact`. Each candidate escalates only when its new logit is greater than zero. These are alternatives, not a confirmed rule.

1. **Output shift:** Use `f(x) + 20e`. EU alerts receive a constant bonus of 20 logit units.
2. **Input re-interpretation:** Use `f(x')`, where `impact' = impact + 0.2e` and every other input stays the same. Do not clip the modified impact; it can reach 1.2 inside this calculation. Every submitted query input stays within the required range.
3. **Interaction:** Use `f(x) + 40ei`. The impact bonus depends on region. EU alerts receive a bonus proportional to impact; other alerts receive zero bonus.

Forward checks confirm that each candidate matches all 32 evidence labels. Each candidate changes rows 1–16 from suppress to escalate and preserves the decisions on rows 17–32. No model weights were changed.

## Query design

Rows 1–4 distinguish the rule types. They use simple feature values and give different decision patterns. Rows 5–6 repeat rows 1–2 with `region_eu = 0` to check the region condition. Features not specified below equal 0.5.

| Query row | impact | urgency | users_affected | tier_critical | maintenance_window | region_eu | Output shift | Input re-interpretation | Interaction |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.9 | 0.1 | 0.5 | 0 | 1 | 1 | 0 | 0 | 1 |
| 2 | 0.3 | 0.9 | 0.1 | 1 | 0 | 1 | 0 | 1 | 0 |
| 3 | 0.7 | 0.5 | 0.5 | 0 | 0 | 1 | 0 | 1 | 1 |
| 4 | 0.1 | 0.7 | 0.9 | 1 | 1 | 1 | 1 | 1 | 0 |
| 5 | 0.9 | 0.1 | 0.5 | 0 | 1 | 0 | 0 | 0 | 0 |
| 6 | 0.3 | 0.9 | 0.1 | 1 | 0 | 0 | 0 | 0 | 0 |

The last three columns are candidate predictions, not supplied labels. Query row numbers refer to data rows, excluding the CSV header.
