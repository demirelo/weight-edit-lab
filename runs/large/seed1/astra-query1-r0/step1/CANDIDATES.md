# Candidate rules

Let `f(x)` be the original model logit. Let `x_zero` contain the same inputs as `x`, with `tone_anger` set to zero. Escalate only when the candidate logit is greater than zero.

1. **Remove tone from the decision.** Use `f(x_zero)` for every input. This rule makes the decision independent of `tone_anger`.
2. **Apply a tone penalty.** Use `f(x) - 64 * tone_anger` for every input. This rule reduces the score in proportion to anger but retains the original model's interactions with tone.

Forward evaluation confirms that each candidate matches all 32 labelled examples. Candidate 1 changes the first 16 labels from 1 to 0 and preserves the last 16 labels. Candidate 2 does the same. These checks establish consistency with the evidence, not the intended rule. No model weights were changed or fitted.

## Selected query

The row in `query.csv` has maximum impact and anger, zero urgency, and a critical tier. The other binary inputs are zero. All remaining inputs are 0.5.

| Candidate | Query logit | Predicted label |
| --- | ---: | ---: |
| Remove tone | 6.134199 | 1 |
| Apply tone penalty | -10.723968 | 0 |

The original query logit is 53.276032. The correct label will distinguish these two candidates with one query. It will not exclude every other possible rule.
