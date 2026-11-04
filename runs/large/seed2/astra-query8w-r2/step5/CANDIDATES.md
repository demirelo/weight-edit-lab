# Step 5 candidates

These are hypotheses, not confirmed rules. Each candidate matches all 32 labels in `evidence.csv`, as checked by forward passes. No model weights were changed or fitted.

## Evidence and limits

The first 16 rows all suppress alerts during maintenance, with `users_affected` between 0.106 and 0.420. A maintenance suppression threshold of 0.5 is plausible. The examples do not establish its exact value or whether strong alerts can escape suppression.

A maintenance-only rule does **not** explain every current label. Rows 18 and 19 have current logits 0.087337 and 0.209502, but both labels are 0. Row 19 has no maintenance window. Both rows have low impact, low error rate, moderate urgency, and a noncritical tier. The candidates include a provisional second condition to account for these observations. It may instead reflect an error in an earlier model edit; the evidence does not establish its cause.

Historical files contain labels at their respective steps. Later corrections can override those labels. The current model already disagrees with some step 1–3 labels; it agrees with all 40 step 4 labels. Each candidate changes step 4 rows 3, 7, and 14, which lie inside the proposed maintenance region, and preserves the other 37 step 4 labels. Historical labels are not all simultaneous final-label constraints.

## Definitions

- `f(x)`: the unchanged `model_in.json` logit.
- `m`: `maintenance_window`; `n`: `users_affected`; `u`: `urgency`.
- `R`: `m = 1` and `n < 0.5`.
- `G`: `tier_critical = 0`, `impact < 0.2`, and `error_rate < 0.5`.
- `W`: `G` and `u < 0.75`.
- `I(condition)`: 1 when the condition is true, otherwise 0.
- `ReLU(t)`: `max(t, 0)`.

All unspecified features retain their original effect. A candidate escalates exactly when its resulting logit is greater than zero.

### A — Region override

Force suppression inside either raw-feature box `R` or `W`. Otherwise use `f(x)`.

For decision purposes, set the candidate logit to zero inside those boxes. This rule suppresses even the strongest alerts inside either box.

### B — Output shift

Use `f(x) - 64 I(R) - 0.25 I(W)`.

The fixed penalties suppress all required current examples. A sufficiently large original logit can still cause escalation. The constants are explicit alternative hypotheses, not estimated true parameters.

### C — Interaction

Use `f(x) - 1024 m ReLU(0.5 - n) - 4 I(G) ReLU(0.75 - u)`.

Maintenance makes suppression depend on the number of affected users. Within `G`, urgency controls a second suppression penalty. These penalties decrease continuously to zero at their respective thresholds. Strong alerts or alerts close to a threshold can still escalate.

## Query predictions

Rows below refer to data rows in `query.csv`. Entries are predicted labels, not oracle answers.

| Row | Purpose | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Test whether a strong maintenance alert escapes a fixed penalty | 0 | 1 | 0 |
| 2 | Test whether suppression weakens near the user threshold | 0 | 0 | 1 |
| 3 | Test whether the provisional second condition is absolute | 0 | 1 | 1 |
| 4 | Separate fixed and urgency-dependent penalties in that condition | 0 | 0 | 1 |
| 5 | Probe the user threshold at 0.45 | 0 | 0 | 1 |
| 6 | Probe the user threshold at exactly 0.5 | 1 | 1 | 1 |
| 7 | Remove maintenance from row 2 | 1 | 1 | 1 |
| 8 | Raise urgency above 0.75 from row 4 | 1 | 1 | 1 |

Rows 1 and 2 distinguish all three rule kinds. Rows 3 and 4 test the additional condition required by the two unexplained labels. Rows 5–8 test thresholds and controls. Oracle answers can reject all three candidates; agreement with the present examples does not prove any candidate.
