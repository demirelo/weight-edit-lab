# Candidate rules

Let `f(x)` be the unchanged model's logit, `t = tone_anger`, and
`c = confidence`. Each candidate escalates exactly when its new score is
strictly greater than zero. These are hypotheses, not confirmed rules.

1. **A — Input re-interpretation:** Set `tone_anger` to zero before applying
   the current model. Score: `f(x with tone_anger = 0)`. This removes tone
   from the decision at every input.
2. **B — Output shift:** Subtract 30 from `f(x)` when `t <= 0.7`; subtract
   45 when `t > 0.7`. This applies a fixed penalty in each tone region.
3. **C — Interaction:** Score: `f(x) - 64*t + min(t, c)`. Confidence reduces
   the tone penalty until it reaches the tone value. This is a feature
   interaction, since the effect of confidence depends on tone. The minimum
   can be expressed with ReLU: `min(t, c) = t - ReLU(t - c)`.

Forward passes confirm that each candidate matches all 32 evidence labels.
Their minimum absolute scores on the evidence are approximately 1.0517,
1.0863, and 0.4101, respectively. A is the leading hypothesis because it
uses a simple input change. The evidence does not establish it uniquely.
No training, parameter fitting, or model editing was used.

## Query predictions

Rows refer to data rows in `query.csv`; 1 means escalate.

| Row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | Separate the interaction from A and B. |
| 2 | 0 | 1 | 0 | Separate the output shift from A and C. |
| 3 | 1 | 0 | 1 | Check the output penalty when tone is zero. |
| 4 | 1 | 1 | 0 | Separate the interaction at high tone. |
| 5 | 0 | 1 | 0 | Check B below its tone threshold. |
| 6 | 0 | 0 | 0 | Check B above its tone threshold, paired with row 5. |
| 7 | 1 | 1 | 0 | Change only tone from row 3 to test tone independence. |
| 8 | 1 | 0 | 1 | Change only tone from row 4 to test tone independence. |

Rows 1–4 separate rule types. Rows 5–6 check the proposed threshold;
rows 3/7 and 4/8 check whether tone can change a decision with other inputs
fixed. Answers can reject all three candidates.
