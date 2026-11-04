# Candidate rules

Let `f(x)` be the unchanged `model_in.json` logit. Escalate when the candidate logit is strictly greater than zero. These are hypotheses, not confirmed rules.

1. **A — Output shift.** Use `f(x) + 20 * region_eu`. EU alerts receive a constant bonus; other alerts retain their current logit.
2. **B — Input re-interpretation.** For EU alerts, replace `impact` with `min(1, impact + 0.2)`, then evaluate the current model. Keep all other inputs unchanged. For other alerts, use `f(x)`.
3. **C — Interaction.** Use `f(x) + 40 * region_eu * impact`. The impact-dependent bonus applies only to EU alerts.

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv`, including all 16 changed labels and all 16 unchanged labels. No training or fitting was used.

The earlier correction appears to remove the effect of `tone_anger`: its entire input-weight row is zero, and the current model matches all 40 historical labels in `evidence_step1.csv`. Each candidate preserves this independence. Historical labels describe step 1; the new EU correction can supersede them, as TASK.md permits.

# Query design

Rows refer to data rows in `query.csv`. All unspecified continuous features equal 0.5.

| Row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | Separate the capped input increase from both bonuses. |
| 2 | 0 | 1 | 0 | Separate the input increase from both bonuses. |
| 3 | 0 | 0 | 1 | Separate the impact-dependent bonus from both alternatives. |
| 4 | 1 | 1 | 0 | Separate the impact-dependent bonus at lower impact. |
| 5 | 0 | 1 | 1 | Separate the constant bonus from both alternatives. |
| 6 | 0 | 1 | 1 | Test a constant bonus near 20.807. |
| 7 | 1 | 1 | 1 | Test a constant bonus near 18.209; pair with row 6. |
| 8 | 0 | 0 | 0 | Check the EU condition; pair with row 1. |

The first three answers give distinct signatures: A = `100`, B = `010`, C = `101`. Different answers can reject all three hypotheses. Rows 6 and 7 differ only in impact. Row 8 differs from row 1 only in EU status.
