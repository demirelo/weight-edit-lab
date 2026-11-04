# Candidate rules

Let `f(x)` be the original model logit. Each candidate predicts escalation if its corrected logit is greater than zero. Both candidates match all 32 labelled examples: they change rows 1–16 to label 0 and keep the labels of rows 17–32.

1. **Remove anger from the input.** Set `tone_anger = 0` before evaluation. Use `f(x with tone_anger = 0)` as the corrected logit. All other inputs keep their supplied values.
2. **Subtract a linear anger contribution.** Use `f(x) - 65 * tone_anger` as the corrected logit. This rule keeps the original model evaluation and subtracts a fixed contribution per unit of anger. The coefficient 65 is a candidate value; the examples do not establish it as the intended value.

# Selected query

`query.csv` copies evidence row 30 and changes only `tone_anger` from 0.650 to 1.000. The original logit is approximately 54.908784.

| Candidate | Corrected logit | Predicted label |
| --- | ---: | ---: |
| Remove anger from the input | 8.609374 | 1 |
| Subtract a linear anger contribution | -10.091216 | 0 |

One returned label separates these two candidates. Other rules can still match the evidence and that label. No model weights were changed.
