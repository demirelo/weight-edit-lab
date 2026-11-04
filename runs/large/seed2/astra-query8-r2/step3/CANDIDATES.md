# Candidate rules for step 3

These are hypotheses, not confirmed corrections. No model weights were changed.

## Evidence and existing behavior

All 14 current examples that change from 0 to 1 have `tier_critical = 1` and `error_rate >= 0.731261`. Current row 28 changes from 1 to 0. It has error rate 0.653966 and latency spike 0.919993. Thus, a rule that only adds escalation cannot match every current label.

The existing model has two nonnegative output branches:
- `B`: the original network branch, with the tone_anger input weights already zero.
- `E = ReLU(impact + urgency + 0.05*tier_critical + 2*region_eu - 3)`: the added EU branch.

The current decision is `B > 0 OR E > 0`. Row 28 has `B = 0` and `E > 0`. The evidence does not establish why this EU-only escalation must stop.

## Four distinct candidates

Each candidate returns 1 exactly when:

`B > 0 OR (E > 0 AND NOT veto) OR (tier_critical = 1 AND error_rate > threshold)`.

Otherwise it returns 0. Each veto applies only when `tier_critical = 1` and `error_rate <= threshold`.

| Candidate | Threshold | Additional veto condition |
|---|---:|---|
| A | 0.70 | latency_spike > 0.90 |
| B | 0.72 | latency_spike > 0.90 |
| C | 0.70 | error_rate > 0.60 |
| D | 0.72 | error_rate > 0.60 |

The thresholds and veto conditions are tentative. All four candidates match all 32 current labels and all 40 step-2 labels, including answered queries. They retain the existing tone independence. Four step-1 labels were already superseded by the step-2 model; no candidate adds a disagreement on step-1 evidence beyond those existing overrides.

## Query design

Rows 1-4 use a neutral context with low impact, urgency, and users affected. The existing model returns 0. Rows 5-8 copy current evidence row 28 and change one feature. Row numbers below exclude the CSV header.

| Query | Change or test | A | B | C | D |
|---|---|---:|---:|---:|---:|
| 1 | error_rate = 0.69; lower control | 0 | 0 | 0 | 0 |
| 2 | error_rate = 0.71; separates thresholds | 1 | 0 | 1 | 0 |
| 3 | error_rate = 0.70; tests strict boundary | 0 | 0 | 0 | 0 |
| 4 | error_rate = 0.72; tests strict boundary | 1 | 0 | 1 | 0 |
| 5 | row 28 with latency_spike = 0.50 | 1 | 1 | 0 | 0 |
| 6 | row 28 with error_rate = 0.50 | 0 | 0 | 1 | 1 |
| 7 | row 28 with latency_spike = 0.8999 | 1 | 1 | 0 | 0 |
| 8 | row 28 with latency_spike = 0.9001 | 0 | 0 | 0 | 0 |

Queries 2 and 5 distinguish all four candidates. The other queries test the proposed boundaries and can reject all four candidates. Predictions are hypotheses, not oracle labels.
