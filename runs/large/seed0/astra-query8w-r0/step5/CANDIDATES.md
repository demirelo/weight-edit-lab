# Candidate rules for step 5

Let `f(x)` be the unchanged model_in.json logit. Escalate only when the candidate logit is greater than zero. Each candidate keeps the current decision when `maintenance_window = 0`.

1. **A — Output shift.** Use `f(x) - 50 * maintenance_window`. Maintenance imposes a fixed penalty, but a sufficiently high logit can still cause escalation.
2. **B — Region override.** Force suppression when `maintenance_window = 1` and `users_affected < 0.5`. Use the current decision elsewhere. The boundary value 0.5 is outside the suppression box.
3. **C — Input re-interpretation.** During maintenance, set `impact = 0` and `tier_critical = 0` before evaluating the current model. Keep all other input values. Outside maintenance, use the original inputs. This treats reported impact and critical tier as inapplicable during maintenance; other signals can still cause escalation.
4. **D — Region override.** Force suppression whenever `maintenance_window = 1`, for all values of the other features. Use the current decision elsewhere.

## Evidence check

Forward passes confirm that each candidate matches all 32 supplied labels. All 20 maintenance examples have label 0. Their largest current logit is about 47.280, so candidate A suppresses them. Candidate C gives a zero logit for each. The maintenance examples outside B's box already have zero logits. All 12 examples outside maintenance retain their labels.

These are hypotheses, not confirmed rules. The evidence does not establish the penalty of 50, the boundary of 0.5, or which inputs maintenance should change.

## Query design

query.csv contains eight valid inputs without labels. Rows 1–2 test whether a high logit can overcome a maintenance penalty. Rows 3–5 separate the limited suppression box from input re-interpretation and unconditional suppression. Rows 6–8 test whether signals that survive input re-interpretation can still cause escalation. Rows 2–4 also probe the proposed users_affected boundary.

Predictions below use 1 for escalation and 0 for suppression. Row numbers exclude the CSV header.

| Query row | A: shift | B: limited box | C: modified inputs | D: all maintenance |
|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 |
| 3 | 1 | 1 | 0 | 0 |
| 4 | 1 | 1 | 0 | 0 |
| 5 | 0 | 1 | 0 | 0 |
| 6 | 0 | 1 | 1 | 0 |
| 7 | 0 | 1 | 1 | 0 |
| 8 | 1 | 1 | 1 | 0 |

Each candidate has a distinct prediction sequence. Correct labels can reject all four candidates; they need not confirm one. No model weights were changed.
