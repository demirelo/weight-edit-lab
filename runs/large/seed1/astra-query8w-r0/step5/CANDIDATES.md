# Candidate rules for step 5

Let `f(x)` be the complete, unchanged `model_in.json` logit, including all earlier corrections. Let `m = maintenance_window` and `u = users_affected`. Escalate only when the candidate logit is strictly greater than zero.

The changed examples suggest suppression during maintenance at low `users_affected`. The labels do not establish the exact boundary or mechanism. These are alternative hypotheses, not confirmed rules.

1. **A — Output shift.** If `m = 1` and `u < 0.50`, use `f(x) - 110`. Otherwise use `f(x)`. A sufficiently high current logit can still cause escalation inside this region.
2. **B — Region override.** If `m = 1` and `u < 0.50`, use `-1` and suppress the alert. Otherwise use `f(x)`. This box places no additional limits on the other features.
3. **C — Interaction.** Use `f(x) - 1200 * m * max(0.55 - u, 0)`. Maintenance adds a suppression penalty whose size decreases as `users_affected` increases. The penalty reaches zero at `u = 0.55`.

Each candidate matches all 32 labels in `evidence.csv`, including the five positive labels. The constants define concrete hypotheses; they are not uniquely determined by the evidence. Checks used forward passes only. No weights were changed or trained.

The first three queries separate the rule types. Later queries test boundaries, penalty strength, and the maintenance condition. All unspecified values are explicitly included in `query.csv`.

| Query row | A | B | C | Purpose |
|---|---|---|---|---|
| 1 | 1 | 0 | 0 | High current logit inside the box: finite penalty versus forced suppression. |
| 2 | 0 | 0 | 1 | Moderate current logit near the box edge: tapered penalty versus A and B. |
| 3 | 1 | 1 | 0 | Outside the box but below the interaction cutoff: C versus A and B. |
| 4 | 0 | 0 | 0 | Just below the proposed box boundary; compare with row 5. |
| 5 | 1 | 1 | 0 | Exactly at the proposed box boundary; tests the strict inequality. |
| 6 | 1 | 1 | 1 | At the interaction cutoff; the penalty is zero. |
| 7 | 1 | 1 | 1 | Maintenance off; matched control for row 1. |
| 8 | 1 | 0 | 1 | Higher users_affected; matched comparison with row 1 at a high current logit. |

These table entries are candidate predictions, not supplied correct labels. The first two queries already give each candidate a distinct prediction sequence. Actual labels may reject all three candidates.
