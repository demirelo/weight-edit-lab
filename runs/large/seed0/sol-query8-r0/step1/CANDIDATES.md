# Candidate rules

Let `f(x)` be the unchanged input model logit. Each candidate escalates if its stated logit is greater than zero. All other input features stay unchanged.

1. **Remove anger.** Use `f(x with tone_anger = 0)` for every input. Anger has no effect on escalation.
2. **Limit anger.** Use `f(x with tone_anger = min(tone_anger, 0.05))`. Anger can affect escalation up to 0.05; larger values have no additional effect.
3. **Remove anger at a threshold.** Use `f(x with tone_anger = 0)` when `tone_anger >= 0.10`; otherwise use `f(x)`. Mild anger keeps its original effect.

Each candidate matches all 32 supplied labels. The input model disagrees with the first 16 labels and agrees with the last 16. Candidate 1 is the leading interpretation. The evidence does not establish the proposed limits of 0.05 or 0.10; these values define distinct alternatives for this query.

## Query predictions

Rows follow the order in `query.csv`. All query rows use 0.5 for features other than impact, anger, and the three binary features. All three binary features are zero.

| Row | impact | tone_anger | Candidate 1 | Candidate 2 | Candidate 3 |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.840 | 0.050 | 0 | 1 | 1 |
| 2 | 0.840 | 0.100 | 0 | 1 | 0 |
| 3 | 0.840 | 0.800 | 0 | 1 | 0 |
| 4 | 0.820 | 0.099 | 0 | 0 | 1 |
| 5 | 0.820 | 0.100 | 0 | 0 | 0 |
| 6 | 0.850 | 0.025 | 0 | 1 | 1 |

Rows 1 and 2 separate all three candidates together. Row 3 tests whether the cap persists at high anger. Rows 4 and 5 test the proposed 0.10 threshold with a second impact value. Row 6 tests mild anger below the proposed cap.

This phase changes no model weights.
