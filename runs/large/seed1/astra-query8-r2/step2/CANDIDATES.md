# Candidate rules

Let `z` be the unchanged `model_in.json` logit, `e` be `region_eu`, and `t` be `tier_critical`. Each candidate escalates exactly when its adjusted logit is greater than zero. Each candidate preserves the original decision outside the EU.

1. **A — EU threshold of -18:** Use `z + 18*e`.
2. **B — EU threshold of -20:** Use `z + 20*e`.
3. **C — EU threshold of -25:** Use `z + 25*e`.
4. **D — EU threshold depends on critical tier:** Use `z + e*(20 + 10*t)`. The threshold is -20 for other tiers and -30 for the critical tier.

All four candidates match all 32 current labels. These are hypotheses, not confirmed rules. The changed examples have EU logits from -17.9453 to -1.1326. The closest EU example that stays negative has logit -27.2970 and is not in the critical tier.

The baseline matches all 40 earlier labels. Its first-layer weights for `tone_anger` are zero. This supports the earlier correction: ignore tone anger. Every candidate preserves that independence. Earlier labels apply before this step; the new rule can override an earlier decision.

## Query predictions

Rows use 0.5 for every feature except impact, critical tier, EU region, and maintenance status.

| Query row | Baseline logit | A | B | C | D |
|---|---:|---:|---:|---:|---:|
| 1 | -19.508106 | 0 | 1 | 1 | 1 |
| 2 | -20.806939 | 0 | 0 | 1 | 0 |
| 3 | -23.387841 | 0 | 0 | 1 | 0 |
| 4 | -25.742250 | 0 | 0 | 0 | 0 |
| 5 | -29.387115 | 0 | 0 | 0 | 1 |
| 6 | -27.206405 | 0 | 0 | 0 | 1 |
| 7 | -19.500576 | 0 | 0 | 0 | 0 |
| 8 | -21.124614 | 0 | 0 | 1 | 0 |

Rows 1, 2, and 5 distinguish all four candidates. Rows 3, 4, and 6 check nearby thresholds. Row 7 checks the EU condition. Row 8 checks whether maintenance changes the result from row 2.

No model weights were changed. Candidate checks used forward passes only.
