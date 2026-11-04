# Candidate rules

All four candidates match all 32 labels in `evidence.csv`. These are hypotheses, not confirmed rules. Rows are numbered from 1 after the header.

## Shared hypothesis outside maintenance

Row 24 has `maintenance_window=0`, but its current logit is approximately 0.0203321 and its label is 0. A maintenance veto alone cannot explain this row.

For each candidate, use the current model with this additional change: for noncritical alerts only, change the urgency threshold in the low-confidence escalation branch from 0.60 to 0.65. Keep the critical-alert branch unchanged. This is a possible explanation, not an established correction.

Precisely, let `B` be the current logit's contribution before the low-confidence branch. Define `r(a)=max(a,0)` and `q=0.65` for `tier_critical=0`, otherwise `q=0.60`. The proposed logit before the maintenance veto is:

`B + min(r(0.4-confidence), r(urgency-0.2), max(r(impact-0.45), r(urgency-q)), 1+tier_critical-maintenance_window)`.

## Four alternatives

1. **C1: Maintenance cutoff 0.50.** Force label 0 when `maintenance_window=1` and `users_affected<0.50`. Otherwise use the shared hypothesis.
2. **C2: Maintenance cutoff 0.60.** Force label 0 when `maintenance_window=1` and `users_affected<0.60`. Otherwise use the shared hypothesis.
3. **C3: Maintenance cutoff 0.75.** Force label 0 when `maintenance_window=1` and `users_affected<0.75`. Otherwise use the shared hypothesis.
4. **C4: All maintenance alerts.** Force label 0 whenever `maintenance_window=1`. Otherwise use the shared hypothesis.

Each veto takes precedence over earlier escalation rules. Historical files contain labels from earlier stages; the task permits later corrections to override them. For example, the veto overrides step 4 row 36. Outside maintenance, the shared hypothesis preserves all step 4 labels. Earlier-stage labels are not treated as simultaneous final labels.

## Query purpose and predictions

Rows 1–6 vary only `users_affected` on a strong positive alert during maintenance. Rows 7–8 use evidence row 24, set `service_age=0.5`, and set urgency to 0.625 or 0.675. They check the shared hypothesis; they do not separate C1–C4. An unexpected answer can reject all four candidates.

| Query row | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 |
| 4 | 1 | 1 | 0 | 0 |
| 5 | 1 | 1 | 0 | 0 |
| 6 | 1 | 1 | 1 | 0 |
| 7 | 0 | 0 | 0 | 0 |
| 8 | 1 | 1 | 1 | 1 |

The existing examples do not establish exact cutoff values or equality behavior. No model file was edited.
