# Candidate rules for step 5

Let `f(x)` be the unchanged `model_in.json` logit. Escalate only when the candidate logit is greater than zero. Let `m = maintenance_window` and `u = users_affected`.

These are hypotheses. Each matches all 32 labels in `evidence.csv`. The examples do not establish a unique rule or exact boundary.

1. **A — Output shift.** If `m = 1` and `u < 0.5`, subtract 100 from `f(x)`. Else, use `f(x)`. A sufficiently strong alert can still escalate inside this region.
2. **B — Region override.** If `m = 1` and `u < 0.5`, force label 0. Else, use the current model decision. This box has no restrictions on other features.
3. **C — Interaction.** Use the logit `f(x) - 1000 * m * max(0, 0.6 - u)`. Maintenance reduces the logit more when fewer users are affected. The penalty becomes zero at `u = 0.6`.

The constants are explicit candidate assumptions, not inferred facts. No model weights were changed, trained, or fitted.

## Query design

Rows refer to data rows in `query.csv`, excluding its header. Labels below are candidate predictions, not correct labels.

| Row | Purpose | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Strong alert inside the box: distinguish finite shift from forced suppression. | 1 | 0 | 0 |
| 2 | Moderate alert at u = 0.5: distinguish interaction from A and B. | 1 | 1 | 0 |
| 3 | Same moderate alert at u = 0.499: test just below the box boundary. | 0 | 0 | 0 |
| 4 | Same moderate alert at u = 0.501: test just above the box boundary. | 1 | 1 | 0 |
| 5 | Weak positive alert at u = 0.59: test the interaction penalty beyond the box. | 1 | 1 | 0 |
| 6 | Same alert at u = 0.6: test where the interaction penalty ends. | 1 | 1 | 1 |
| 7 | Row 1 with maintenance disabled: check the maintenance condition. | 1 | 1 | 1 |
| 8 | Row 1 at u = 0.5: compare strong and moderate alerts at the same boundary. | 1 | 1 | 1 |

Rows 1 and 2 give distinct prediction pairs for all three rule types. The remaining rows test boundaries, alert strength, and the maintenance condition. All inputs satisfy the feature constraints.
