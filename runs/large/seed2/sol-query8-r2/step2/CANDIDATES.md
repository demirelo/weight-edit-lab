# Candidate rules for step 2

Let `f(x)` be the unchanged `model_in.json` logit. Escalate when the candidate logit is greater than zero, or when an explicit escalation condition below is true.

1. **EU bonus of 20:** Use `f(x) + 20 * region_eu`.
2. **EU bonus of 30:** Use `f(x) + 30 * region_eu`.
3. **Global bonus of 20:** Use `f(x) + 20`.
4. **EU combined-severity condition:** Escalate if `f(x) > 0`, or if `region_eu == 1` and `impact + urgency >= 0.95`.

Each candidate matches all 32 current labels. The 16 changed examples have `region_eu == 1` and original logits between -18.218 and -0.278. The unchanged EU negatives have logits below -39.29. The unchanged non-EU negatives have logits below -30.33. All changed examples also have `impact + urgency > 0.974`.

The earlier correction appears to remove dependence on `tone_anger`. Earlier paired queries keep the same label when only anger changes. The input model also has zero weights for this feature. Every candidate retains that independence. Later step-2 rules may override earlier labels.

## Query design

Rows use existing examples as controlled starting points. The table gives predictions, not known labels. Query row numbers exclude the header.

| Query | Purpose | EU +20 | EU +30 | Global +20 | EU severity |
| --- | --- | --- | --- | --- | --- |
| 1 | Probe the larger EU bonus | 0 | 1 | 0 | 1 |
| 2 | Probe near the smaller EU bonus | 0 | 1 | 0 | 1 |
| 3 | Probe above the smaller EU boundary | 1 | 1 | 1 | 1 |
| 4 | Test high severity with a low original logit | 0 | 0 | 0 | 1 |
| 5 | Test low severity with a moderate original logit | 1 | 1 | 1 | 0 |
| 6 | Test the regional scope at a moderate logit | 0 | 0 | 1 | 0 |
| 7 | Test the regional scope at a higher logit | 0 | 0 | 1 | 0 |
| 8 | Test low severity between the two EU boundaries | 0 | 1 | 0 | 0 |

No model weights were changed. Candidate checks used forward passes only.
