# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Escalate only when the candidate logit is greater than zero. Let `e = region_eu`, `u = urgency`, and `c = confidence`.

The first 16 current examples change from suppress to escalate. All have `e = 1`. Their original logits range from -16.17247 to -1.30729. The other 16 examples keep their original decisions. For an EU-only constant bonus, the current evidence permits `16.17247 < bonus <= 22.13732`.

## A. Output shift

Use `f(x) + 18*e`. EU alerts receive a constant logit bonus of 18. Other alerts keep their original logits.

## B. Input re-interpretation

Replace urgency with `min(1, u + 0.22*e)`, then apply the current model. Keep all other inputs unchanged. This rule increases urgency for EU alerts, with a cap at 1.

## C. Interaction

Use `f(x) + e*(17 + 2*c)`. Confidence controls the EU bonus, which ranges from 17 to 19. Other alerts keep their original logits.

## Evidence checks

Each candidate matches all 32 labels in `evidence.csv`, including every unchanged case. These are alternative hypotheses, not confirmed rules. Forward passes checked the stated formulas. No model training or weight changes occurred.

The inferred earlier correction removes the effect of `tone_anger`. All first-layer weights for that input are zero, and the current model matches all 40 earlier examples. Each candidate preserves this independence. Earlier labels describe the earlier step; the new correction may override an earlier decision, as TASK.md permits.

## Query design

Rows 1–4 separate the three rule types. Rows 5–8 test bonus values within the interval allowed by the evidence. Under a constant EU bonus, each row escalates exactly when the bonus exceeds the negative of its original logit.

| Query row | Original logit | A | B | C | Purpose |
|---|---:|---:|---:|---:|---|
| 1 | -20.058520 | 0 | 1 | 0 | Separate the urgency increase from both bonuses. |
| 2 | -9.424273 | 1 | 0 | 1 | Test the urgency cap at urgency 1. |
| 3 | -18.449851 | 0 | 0 | 1 | Test the larger bonus at high confidence. |
| 4 | -17.443567 | 1 | 1 | 0 | Test the smaller bonus at low confidence. |
| 5 | -16.499863 | 1 | 1 | 1 | Test a bonus near the lower evidence bound. |
| 6 | -17.993753 | 1 | 0 | 1 | Test a bonus just below 18. |
| 7 | -18.005008 | 0 | 1 | 0 | Test a bonus just above 18. |
| 8 | -21.500021 | 0 | 0 | 0 | Test a bonus near the upper evidence bound. |

Table labels are candidate predictions. They are not oracle answers. Query inputs were selected through forward passes on valid constructed inputs. All eight rows use the required feature order and contain no label column.
