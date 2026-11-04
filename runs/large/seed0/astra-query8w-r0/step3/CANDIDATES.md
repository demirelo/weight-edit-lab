# Candidate rules for step 3

Let `F(x)` be the unchanged logit from `model_in.json`. Escalate when the candidate logit is strictly positive. Let `e = error_rate` and `t = tier_critical`.

The current model disagrees with rows 1–16 of `evidence.csv`. Each row has `t = 1` and `e >= 0.739`. All 16 require escalation. The examples do not establish a unique rule or threshold.

## A. Output shift

Add a fixed bonus of 100 to `F(x)` when `t = 1` and `e > 0.70`. Otherwise use `F(x)`.

This bonus can leave a sufficiently negative logit below zero.

## B. Region override

Force escalation when `t = 1` and `e > 0.70`, for all values of the other features. Otherwise use the current decision.

This rule overrides even a very negative logit.

## C. Interaction

Use `F(x) + 1200 * t * max(e - 0.70, 0)`.

The added effect of error rate depends on critical tier. The bonus grows with error rate instead of staying fixed. For binary `t`, the added term also equals `1200 * ReLU(e + t - 1.70)`.

## Evidence check

Each candidate matches all 32 labels in `evidence.csv`, including the 16 unchanged cases. The values 0.70, 100, and 1200 define testable hypotheses; they are not confirmed rule parameters. Forward passes checked the candidates. No training, fitting, or model edit was performed.

## Query design

Rows below refer to data rows in `query.csv`. Predictions are hypotheses, not supplied labels. Queries 1–3 separate all three kinds. Queries 4–7 test the threshold. Query 8 tests the tier condition. Other features equal 0.5, except `region_eu` and `maintenance_window`, which equal 0.

| Query | Purpose | Current logit | A | B | C |
|---|---|---:|---:|---:|---:|
| 1 | Low impact, urgency, and users; error 0.75: test override | -101.579784 | 0 | 1 | 0 |
| 2 | Moderate impact, urgency, and users; error 0.75: test fixed bonus | -69.915995 | 1 | 1 | 0 |
| 3 | Low impact, urgency, users, and latency; error 0.90: test growing bonus | -112.115942 | 0 | 1 | 1 |
| 4 | Error 0.60: test a lower threshold | -74.536290 | 0 | 0 | 0 |
| 5 | Error 0.699: test below 0.70 | -71.710075 | 0 | 0 | 0 |
| 6 | Error 0.700: test equality | -71.680324 | 0 | 0 | 0 |
| 7 | Error 0.701: test above 0.70 | -71.650573 | 1 | 1 | 0 |
| 8 | Error 0.90, noncritical tier: test tier condition | -89.195405 | 0 | 0 | 0 |

The first three prediction sequences are A = `010`, B = `111`, and C = `001`. Thus each candidate has a distinct sequence. Labels that differ from all candidate sequences will require a new hypothesis.
