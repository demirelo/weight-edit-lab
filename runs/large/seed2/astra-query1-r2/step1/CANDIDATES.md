# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Both candidates keep all other input features unchanged and escalate only when the resulting logit is greater than zero.

1. **Remove the tone effect.** Evaluate `f(x)` with `tone_anger = 0` for every input. Tone must have no effect on escalation.
2. **Reduce the tone effect.** Evaluate `f(x)` with `tone_anger = 0.02 * original tone_anger` for every input. Tone retains a small effect on escalation.

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv`. These are hypotheses; the examples do not establish either rule for all inputs. The factor 0.02 is a proposed alternative, not an inferred exact value.

## Query

The single query copies evidence row 16 (counting data rows from one) and changes only `tone_anger` to 1.

| Candidate | Query logit | Predicted label |
| --- | ---: | ---: |
| Remove the tone effect | -1.660318678 | 0 |
| Reduce the tone effect | 0.367889130 | 1 |

The answer separates these two candidates. One binary answer cannot identify every possible rule.

The model has not been edited or trained.
