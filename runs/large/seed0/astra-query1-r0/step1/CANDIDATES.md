# Candidate rules

Let `f(x)` be the logit from the unchanged `model_in.json`. Each rule
escalates exactly when its resulting logit is greater than zero.

1. **Remove the effect of anger.** Evaluate `f(x)` with `tone_anger` set
   to `0`. Keep all other input values unchanged.
2. **Limit the effect of anger.** Evaluate `f(x)` with `tone_anger` set
   to `min(tone_anger, 0.05)`. Keep all other input values unchanged.

Both rules match all 32 labelled examples. Each changes the first 16
labels from 1 to 0 and preserves the last 16 labels. Forward passes
confirm these results. Neither rule is confirmed by the evidence alone.

The single input in `query.csv` separates the rules:

| Rule | Predicted logit | Predicted label |
| --- | ---: | ---: |
| Remove the effect of anger | -1.856583 | 0 |
| Limit the effect of anger | 2.328002 | 1 |

A returned label of 0 supports rule 1 over rule 2. A returned label of 1
supports rule 2 over rule 1. Other rules can still fit the evidence.
The model has not been changed.
