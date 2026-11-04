# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Escalate if the candidate logit is greater than zero. Define `G` as `tier_critical = 1` and `error_rate >= 0.70`.

All four candidates match all 32 labels in `evidence.csv`, as checked with forward passes. Each uses the complete current model, including its earlier corrections. Earlier evidence has labels from earlier steps; this correction can override those labels where it applies.

1. **C1 — Output shift:** Use `f(x) + 100` inside `G`. Use `f(x)` elsewhere. A fixed bonus can leave a sufficiently negative alert suppressed.
2. **C2 — Region override:** Force escalation inside `G`, for all values of the other features. Use the current decision elsewhere.
3. **C3 — Interaction:** Use `f(x) + 1000 * tier_critical * max(error_rate - 0.70, 0)`. The error-rate bonus increases with error rate and applies only to critical-tier alerts.
4. **C4 — Input re-interpretation:** Inside `G`, evaluate the current model with `impact` replaced by `impact + 1`. Use the original inputs elsewhere. Do not clip the modified internal value; submitted inputs remain within the required range.

The constants are explicit hypotheses, not established values. The examples locate a possible error-rate boundary between approximately 0.532 and 0.739; they do not establish 0.70 or its inclusion.

## Query design

Rows 1–3 separate the four kinds before testing the boundary. The predicted labels are:

| Query row | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 0 |
| 2 | 1 | 1 | 1 | 0 |
| 3 | 1 | 1 | 0 | 0 |
| 4 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 |
| 6 | 1 | 1 | 0 | 1 |
| 7 | 1 | 1 | 0 | 1 |
| 8 | 0 | 0 | 0 | 0 |

Rows 4–7 hold the other inputs fixed and test error rates 0.60, 0.699, 0.700, and 0.701. These labels test the proposed boundary and its inclusion. Row 8 tests whether a high error rate also changes a noncritical alert.

These candidates do not exhaust the possible rules. Labels that reject all four will guide revised candidates in phase 2.
