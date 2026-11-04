# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Each candidate escalates if its logit is greater than zero. Each candidate changes only the `tone_anger` input used by `f`; it preserves all other inputs.

1. **A: Remove anger dependence.** Evaluate `f` with `tone_anger = 0` for every input. This is the leading hypothesis.
2. **B: Remove anger dependence above a threshold.** Set `tone_anger = 0` when its supplied value is at least `0.2`. Otherwise, use the supplied value. This rule preserves the original model below the threshold.
3. **C: Cap the anger contribution.** Evaluate `f` with `tone_anger = min(tone_anger, 0.01)`. This rule retains a small anger contribution.

Forward passes confirm that each candidate matches all 32 evidence labels. The original model disagrees with labels on rows 1–16 and agrees on rows 17–32. All supplied anger values exceed `0.2`. The evidence therefore does not establish whether anger must be removed at lower values. It also does not exclude a small residual contribution. The thresholds above specify testable alternatives; the evidence does not establish their exact values.

## Query design

The eight query rows use evidence row 16 as a common base. Only `impact` and `tone_anger` change. Rows 1–3 test the threshold in B. Rows 4–8 test whether a small anger contribution remains, with row 4 as a zero-anger control.

| Query row | impact | tone_anger | A label | B label | C label |
|---|---:|---:|---:|---:|---:|
| 1 | 0.925 | 0.1 | 0 | 1 | 0 |
| 2 | 0.925 | 0.199 | 0 | 1 | 0 |
| 3 | 0.925 | 0.2 | 0 | 0 | 0 |
| 4 | 0.933 | 0 | 0 | 0 | 0 |
| 5 | 0.933 | 0.01 | 0 | 1 | 1 |
| 6 | 0.933 | 0.1 | 0 | 1 | 1 |
| 7 | 0.933 | 0.2 | 0 | 0 | 1 |
| 8 | 0.933 | 1 | 0 | 0 | 1 |

These are candidate predictions, not confirmed query labels. Each candidate predicts a distinct answer sequence. No model weights were changed or trained.
