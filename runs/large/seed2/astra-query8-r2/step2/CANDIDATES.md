# Candidate rules

Let `B(x)` be the current model decision: `logit(model_in, x) > 0`.
Let `s = impact + urgency`. Each candidate returns 1 when its condition
below is true. Otherwise, it returns `B(x)`.

1. **A: EU sum above 0.95.** `region_eu == 1` and `s > 0.95`.
2. **B: EU sum above 0.97.** `region_eu == 1` and `s > 0.97`.
3. **C: EU weighted sum.** `region_eu == 1` and
   `1.1 * impact + urgency > 1.00`.
4. **D: EU sum with a critical-tier exception.** `region_eu == 1` and
   either `s > 1.00`, or both `tier_critical == 1` and `s > 0.95`.

These are hypotheses. All four match all 32 current labels. The evidence
does not establish the exact threshold or whether equality triggers escalation.

The current model also matches all 40 earlier examples and query answers.
Its input weights for `tone_anger` are all zero. This supports the inference
that the earlier correction removed the effect of anger. Each candidate
preserves this property. Earlier labels apply to the earlier step; the new
correction can override them where its condition applies.

# Query design

All eight queries have negative current logits. Thus, the current model
does not hide a difference between the candidate conditions. Features other
than impact, urgency, and tier remain fixed: `region_eu = 1`,
`maintenance_window = 0`, and all other continuous features equal 0.5.

| Query row | impact | urgency | tier_critical | A | B | C | D |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.48 | 0.48 | 0 | 1 | 0 | 1 | 0 |
| 2 | 0.05 | 0.91 | 0 | 1 | 0 | 0 | 0 |
| 3 | 0.90 | 0.06 | 0 | 1 | 0 | 1 | 0 |
| 4 | 0.49 | 0.49 | 0 | 1 | 1 | 1 | 0 |
| 5 | 0.49 | 0.49 | 1 | 1 | 1 | 1 | 1 |
| 6 | 0.4745 | 0.4745 | 0 | 0 | 0 | 0 | 0 |
| 7 | 0.4755 | 0.4755 | 0 | 1 | 0 | 0 | 0 |
| 8 | 0.90 | 0.02 | 0 | 0 | 0 | 1 | 0 |

Rows 1–3 compare sums of 0.96 with different feature values. Rows 4–5
test the critical-tier exception. Rows 6–7 bracket 0.95 and test whether
the candidate set needs revision. Row 8 tests the weighted-sum rule below
both unweighted thresholds. The columns contain predictions, not supplied
answers.
