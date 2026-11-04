# Candidate rules

Let B(x) be the current model decision: `logit(model_in, x) > 0`.
Each candidate keeps B(x), but forces escalation when its condition is true:

1. **A:** `tier_critical = 1` and `error_rate > 0.68`.
2. **B:** `tier_critical = 1` and `error_rate > 0.70`.
3. **C:** `tier_critical = 1` and `error_rate > 0.72`.
4. **D:** `tier_critical = 1` and `error_rate + 0.10 * latency_spike > 0.75`.

Each complete rule is `B(x) OR condition`. All four match every one of the
32 labelled examples, as checked with forward passes. These are hypotheses;
the examples do not establish a unique rule. No weights were changed or fitted.

## Query design

The queries copy evidence row 12 (counting data rows from 1), then change only
error_rate and latency_spike. The current model rejects all eight queries.
Rows 1–3 separate the three error thresholds. Rows 4–5 test the latency term.
Rows 6–8 test exact threshold values. All comparisons above are strict.

| Query row | Error rate | Latency spike | A | B | C | D |
|---|---|---|---|---|---|---|
| 1 | 0.690 | 0.000 | 1 | 0 | 0 | 0 |
| 2 | 0.710 | 0.000 | 1 | 1 | 0 | 0 |
| 3 | 0.730 | 0.000 | 1 | 1 | 1 | 0 |
| 4 | 0.670 | 0.900 | 0 | 0 | 0 | 1 |
| 5 | 0.690 | 0.800 | 1 | 0 | 0 | 1 |
| 6 | 0.680 | 0.000 | 0 | 0 | 0 | 0 |
| 7 | 0.700 | 0.000 | 1 | 0 | 0 | 0 |
| 8 | 0.720 | 0.000 | 1 | 1 | 0 | 0 |
