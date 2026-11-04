# Candidate rules

Let `z(x)` be the unchanged `model_in.json` logit. Escalate when the candidate logit is greater than zero. Define region `R` as `tier_critical = 1` and `error_rate >= 0.700`. All three candidates match all 32 current labels and all 80 labels in `evidence_step1.csv` and `evidence_step2.csv`. The examples do not establish a unique rule or an exact threshold.

1. **Region override:** Force escalation throughout `R`. Elsewhere, retain `z(x) > 0`. This rule has no dependence on the original logit inside `R`.

2. **Output shift:** Add a constant bonus of `120` to `z(x)` inside `R`. Elsewhere, retain `z(x)`. A sufficiently negative original logit can still prevent escalation.

3. **Interaction:** Add `150 * error_rate` to `z(x)` inside `R`. Elsewhere, retain `z(x)`. The critical-tier bonus increases with error rate. A sufficiently negative original logit can still prevent escalation.

The bonus values are explicit candidate assumptions. The evidence does not uniquely determine them. No weights were changed or fitted.

## Query predictions

Rows 1-3 separate the three rule kinds. Rows 4-5 test the proposed error threshold. Row 6 tests the critical-tier condition. Row numbers refer to data rows in `query.csv`.

| Row | Purpose | Original logit | Region override | Output shift | Interaction |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | Low error boundary; severe negative logit | -132.191543 | 1 | 0 | 0 |
| 2 | Low error boundary; moderate negative logit | -106.609994 | 1 | 1 | 0 |
| 3 | Maximum error; severe negative logit | -127.057820 | 1 | 0 | 1 |
| 4 | Just below error threshold | -132.191561 | 0 | 0 | 0 |
| 5 | Just above error threshold | -132.191525 | 1 | 0 | 0 |
| 6 | Maximum error; noncritical tier | -131.453377 | 0 | 0 | 0 |

Predictions are hypotheses, not supplied correct labels. All unspecified feature values are explicit in `query.csv`.
