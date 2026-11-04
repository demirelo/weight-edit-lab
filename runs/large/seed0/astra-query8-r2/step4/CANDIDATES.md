# Candidate rules for step 4

These are hypotheses, not confirmed rules. Each matches all 32 labels in `evidence.csv`, including the 16 changed labels and 16 unchanged labels. I checked them with forward passes. I did not train or edit the model.

Let `old(x)` mean `model_in.json` returns a logit greater than zero. Each candidate predicts escalation when `old(x)` is true OR its condition below is true. Otherwise, it preserves the current decision. Earlier evidence records labels at earlier steps; a new override can change those labels, as TASK.md permits.

| Candidate | New escalation condition |
| --- | --- |
| A | `confidence < 0.4` AND `maintenance_window == 0` AND `urgency > 0.2` AND (`impact > 0.45` OR `urgency > 0.6`) |
| B | Same as A, but use `confidence < 0.5`. |
| C | Same as A, but remove the maintenance condition. |
| D | Same as A, but use `impact > 0.4`. |

The examples do not establish these exact thresholds or this condition structure. Other rules can also match them. Returned labels can reject all four candidates.

## Query design

Rows use the feature order from `evidence.csv`. All eight have current-model logit zero. Thus, the existing escalation decision does not hide candidate differences. The low error rate also keeps the earlier critical-tier override inactive.

| Query rows | Difference tested | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1–2 | Confidence 0.45 with high urgency; vary tier and region. | 0 | 1 | 0 | 0 |
| 3–4 | Maintenance active with low confidence and high urgency; vary tier and region. | 0 | 0 | 1 | 0 |
| 5–6 | Impact 0.425 with urgency 0.3; vary region. | 0 | 0 | 0 | 1 |
| 7–8 | Impact 0.425 with urgency 0.59; vary region. | 0 | 0 | 0 | 1 |

Labels in this table are candidate predictions, not oracle answers. Paired rows also test whether tier, region, or urgency changes the proposed rule.
