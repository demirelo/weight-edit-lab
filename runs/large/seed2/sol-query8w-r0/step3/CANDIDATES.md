# Candidate rules for step 3

These are hypotheses. Each rule matches all 32 labels in evidence.csv. No model weights were changed.

Let f(x) be the current model logit. The current decision is 1 if f(x) > 0, otherwise 0. Let G mean tier_critical = 1 and error_rate > 0.70.

1. **C1 — Output shift.** Use f(x) + 80 inside G. Use f(x) elsewhere. Apply the usual logit > 0 decision. The bonus can leave alerts with very negative current logits suppressed.
2. **C2 — Region override.** Force decision 1 inside G. Use the current decision elsewhere. Other features do not affect the decision inside G.
3. **C3 — Input re-interpretation.** Inside G, set urgency = 1 and users_affected = 1 before applying the current model. Keep every other input value. Outside G, apply the current model to the original inputs. This rule can still suppress alerts inside G.

The threshold 0.70 is a candidate value. The evidence does not identify the exact threshold. The input changes in C3 are a proposed interpretation, not an established rule.

# Query design

Rows 1–3 separate the three rule types. Rows 4–7 test the error-rate boundary with fixed inputs. Row 8 tests whether the correction requires tier_critical = 1. Predictions below are hypotheses, not correct labels.

| Query row | Current logit | C1 | C2 | C3 | Purpose |
|---|---:|---:|---:|---:|---|
| 1 | -86.161 | 0 | 1 | 1 | Separate a finite bonus from the other rules. |
| 2 | -65.061 | 1 | 1 | 0 | Separate input re-interpretation from the other rules. |
| 3 | -101.536 | 0 | 1 | 0 | Test an override when both other rules suppress. |
| 4 | -95.417 | 0 | 0 | 0 | Test error_rate = 0.69. |
| 5 | -95.255 | 0 | 0 | 0 | Test error_rate = 0.70 exactly. |
| 6 | -95.101 | 0 | 1 | 1 | Test error_rate = 0.71. |
| 7 | -94.806 | 0 | 1 | 1 | Test error_rate = 0.73. |
| 8 | -106.353 | 0 | 0 | 0 | Test tier_critical = 0 at error_rate = 0.90. |
