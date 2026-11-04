# Candidate rules for step 5

Let `z(x)` be the unchanged `model_in.json` logit, `m` be
`maintenance_window`, and `u` be `users_affected`. Escalate only when the
candidate logit is greater than zero. These are hypotheses, not confirmed rules.

1. **A — Output shift.** When `m = 1` and `u < 0.45`, use
   `z(x) - 1100`. Otherwise, use `z(x)`. A sufficiently large original logit
   can still cause escalation.
2. **B — Region override.** Force label 0 when `m = 1` and `u < 0.45`.
   Otherwise, keep the original decision.
3. **C — Interaction.** Use
   `z(x) - 40000 * m * max(0.45 - u, 0)`.
   Maintenance makes lower user impact reduce the logit. The reduction tends
   to zero as `u` approaches 0.45 from below.
4. **D — Region override with a wider range.** Force label 0 when `m = 1`
   and `u < 0.50`. Otherwise, keep the original decision.

All four candidates match all 32 labels in `evidence.csv`. Each rule starts
from the current model, which includes the earlier corrections. A new rule
can override an earlier decision where its condition applies. Earlier-step
labels describe earlier stages; they are not all current labels.

The first 16 examples all have `m = 1`, `u < 0.45`, and label 0.
The current model escalates 15 of them. The remaining examples do not
distinguish these four rules.

## Query predictions

Rows refer to `query.csv`. Predictions are candidate labels, not answers.

| Row | A | B | C | D | Purpose |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | Separate a finite output shift from suppression. |
| 2 | 1 | 0 | 1 | 0 | Separate the interaction from the overrides. |
| 3 | 0 | 0 | 1 | 0 | Confirm the interaction with a smaller original logit. |
| 4 | 1 | 1 | 1 | 0 | Test the exact 0.45 boundary. |
| 5 | 1 | 1 | 1 | 0 | Test between the proposed override thresholds. |
| 6 | 1 | 1 | 1 | 1 | Check the exact 0.50 boundary. |
| 7 | 1 | 0 | 0 | 0 | Test just below the interaction's decision boundary. |
| 8 | 1 | 0 | 1 | 0 | Test just above the interaction's decision boundary. |

Only forward passes were used. No weights were changed or fitted.
