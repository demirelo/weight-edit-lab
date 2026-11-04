# Candidate rules

Let `f(x)` be the logit from the unchanged `model_in.json`, `m` be
`maintenance_window`, and `u` be `urgency`. Escalate only when the candidate
logit is greater than zero.

All four candidates match all 32 labelled examples. The evidence has 21
maintenance rows, all labelled 0. The current model escalates 15 of these rows.
The other 11 rows have `m = 0` and retain the current model's labels.

1. **A — Output shift.** Use `f(x) - 120*m`. Maintenance subtracts a fixed
   120 from the current logit. A sufficiently high logit can still escalate.
2. **B — Region override.** Force label 0 throughout the raw-input box
   `m = 1`, with every other feature unrestricted within its allowed range.
   Use `f(x)` when `m = 0`.
3. **C — Input re-interpretation.** When `m = 1`, replace `urgency` and
   `error_rate` with zero, then evaluate the current model on those modified
   inputs. Keep every other feature unchanged. Use the original inputs when
   `m = 0`.
4. **D — Interaction.** Use `f(x) - 150*m*u`. Maintenance adds an urgency
   penalty: the penalty is zero at urgency 0 and increases with urgency.

These are alternative hypotheses. The evidence does not establish the
constants 120 and 150 or select a unique rule. Forward-pass checks verify
consistency; no model weights were changed or fitted.

# Query design

Rows 1–3 separate the four rule kinds. Each row produces label 1 under exactly
one of A, C, and D. Candidate B produces label 0 for all three. Rows 4–6 repeat
rows 1–3 with maintenance disabled to check the proposed condition.

The table gives predictions, not supplied labels. Row numbers exclude the CSV
header.

| Query row | Current logit | A | B | C | D |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 130.029830 | 1 | 0 | 0 | 0 |
| 2 | 83.953012 | 0 | 0 | 1 | 0 |
| 3 | 41.979296 | 0 | 0 | 0 | 1 |
| 4 | 130.715413 | 1 | 1 | 1 | 1 |
| 5 | 82.991599 | 1 | 1 | 1 | 1 |
| 6 | 42.763629 | 1 | 1 | 1 | 1 |

If returned labels differ from every candidate's predictions, revise the
candidate set before any model edit.

## Phase 2 revision

The supplied answers are `1,1,1,1,1,1`. Thus none of A–D survives.
All three maintenance queries have `users_affected = 1`. Every newly
suppressed example that the input model escalates has `users_affected < 0.5`.
Earlier evidence also contains maintenance alerts with more affected users
that retain label 1, plus a maintenance probe at exactly 0.5 with label 0.

**E — Conditional region override:** suppress when `maintenance_window = 1`
and `users_affected <= 0.5`; otherwise preserve the input model's decision.
This rule matches all 32 current examples and all six supplied answers.
The finite evidence does not uniquely identify the threshold; 0.5 is the
inferred boundary. This edit preserves the existing model outside that region,
including its two pre-existing disagreements with earlier evidence.
