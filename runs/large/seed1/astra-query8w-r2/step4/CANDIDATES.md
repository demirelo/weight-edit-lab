# Candidate rules for step 4

Let `f(x)` be the unchanged logit from `model_in.json`. The current decision is `f(x) > 0`. Let `i`, `u`, `a`, and `c` mean impact, urgency, users_affected, and confidence. All inequalities below are strict.

Each candidate matches all 32 labels in `evidence.csv`, including all 15 changed decisions. These are hypotheses, not confirmed rules. No weights were changed or fitted.

## A — Region override

Force escalation in either of these two raw-feature boxes:

- `c < 0.4` and `u > 0.6`.
- `c < 0.4`, `i > 0.6`, and `a > 0.4`.

All unspecified features can take any permitted value. Outside these boxes, keep the current decision.

## B — Input re-interpretation

When `c < 0.4`, replace impact with `min(1, i + u)`. Keep every other input unchanged. Apply the current model to this modified input and escalate if its logit is positive. When `c >= 0.4`, apply the current model to the original input.

This rule treats urgency as additional impact when confidence is low. The model still decides whether the increased impact warrants escalation.

## C — Interaction

Keep every current escalation. Also escalate when:

`c < 0.4 AND (u > 0.6 OR (i > 0.6 AND u * a > 0.08))`.

For the high-impact branch, the required users_affected value depends on urgency. This gives a curved boundary, unlike A's fixed boxes. For example, urgency 0.4 requires users_affected above 0.2; urgency 0.2 requires users_affected above 0.4.

## Query design

The row numbers below exclude the CSV header. All eight queries have current logit zero. Predictions use `1` for escalate and `0` for suppress.

| Row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | Separate the input change from both override rules. |
| 2 | 1 | 0 | 0 | Separate the fixed boxes from the other rules. |
| 3 | 0 | 0 | 1 | Separate the interaction from the other rules. |
| 4 | 1 | 0 | 1 | Test forced escalation at high urgency and low impact. |
| 5 | 0 | 1 | 0 | Test confidence just below 0.4, using row 1's inputs. |
| 6 | 0 | 0 | 0 | Test confidence just above 0.4, using row 1's inputs. |
| 7 | 0 | 0 | 0 | Test the interaction product just below 0.08. |
| 8 | 0 | 0 | 1 | Test the interaction product just above 0.08. |

Rows 1–3 give each candidate a distinct prediction pattern. Rows 5–8 test proposed values after the rule types have been separated. Answers can reject all three candidates.

Historical labels in `evidence_step1.csv` through `evidence_step3.csv` describe earlier stages, as specified in TASK.md. They are not additional step-4 labels. Relative to the current model, A changes 6/1/1 historical rows, B changes 6/3/2, and C changes 5/1/1, respectively. These are proposed step-4 overrides, not claims that the old labels already confirm them. Each candidate uses the current model outside its stated change.
