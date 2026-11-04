# Candidate rules for step 4

These are hypotheses. Each rule matches all 32 labels in `evidence.csv`, including all 16 changed decisions. The labels do not identify one rule. No model weights were changed.

Let `z(x)` be the logit from `model_in.json`. Let `p = impact`, `u = urgency`, `c = confidence`, and `e = error_rate`. Define:

`G = (c < 0.4) AND (u >= 0.3 OR p >= 0.9)`.

1. **A: Output shift.** Use `z_A(x) = z(x) + 60` when G is true. Otherwise use `z(x)`. Escalate when `z_A(x) > 0`.
2. **B: Region override.** Force escalation in the union of these four boxes: `(c < 0.4 AND u >= 0.65)`, `(c < 0.4 AND p >= 0.9)`, `(c < 0.4 AND p >= 0.7 AND u >= 0.3)`, or `(c < 0.4 AND e >= 0.95 AND u >= 0.3)`. Each box leaves all other features unrestricted within their allowed ranges. Outside these boxes, use `z(x) > 0`.
3. **C: Interaction.** Use `z_C(x) = z(x) + 80 * max(p, u)` when G is true. Otherwise use `z(x)`. Escalate when `z_C(x) > 0`. The bonus depends on both the confidence condition and the larger of impact and urgency.

All three rules retain the current model as their baseline. They do not use tone_anger and do not suppress an existing escalation. Thus, they retain the model's independence from tone_anger and its critical-tier escalation rule. Earlier CSV labels describe earlier stages; a later correction can override those labels, as TASK.md states.

## Query design

Rows are numbered from 1 after the CSV header. Predictions use 1 for escalate and 0 for suppress.

| Row | Purpose | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Separate a forced escalation from both finite bonuses | 0 | 1 | 0 |
| 2 | Separate the constant bonus from the other rules | 1 | 0 | 0 |
| 3 | Separate the larger interaction bonus from the constant bonus | 0 | 1 | 1 |
| 4 | Check confidence just below 0.4 | 1 | 1 | 1 |
| 5 | Check confidence just above 0.4; compare with row 4 | 0 | 0 | 0 |
| 6 | Check urgency just below 0.3 | 0 | 0 | 0 |
| 7 | Check urgency just above 0.3; compare with row 6 | 1 | 1 | 1 |
| 8 | Check impact below 0.9 with low urgency | 0 | 0 | 0 |

Rows 1–3 separate the rule kinds first. Rows 4–8 test the proposed conditions. An answer can reject all three candidates; the thresholds remain unconfirmed.
