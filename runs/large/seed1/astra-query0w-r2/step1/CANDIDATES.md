# Candidate rules

Let `f(x)` be the unchanged model's logit, `a = tone_anger`, and
`c = confidence`. Each candidate escalates if its new logit is greater than
zero. These rules apply throughout the input domain.

1. **Input re-interpretation — ignore anger.** Set `tone_anger` to zero,
   keep all other inputs unchanged, and evaluate the original model:
   `g(x) = f(x with tone_anger = 0)`.
2. **Output shift — increase the escalation threshold.** Subtract 40 from
   the original logit when `a <= 0.75`; subtract 45 when `a > 0.75`.
   Thus, `g(x) = f(x) - 40 - 5 * indicator(a > 0.75)`.
3. **Interaction — confidence reduces the anger penalty.** Apply
   `g(x) = f(x) - 70 * a * (1 - c / 10)`.
   The penalty per unit of anger decreases from 70 at zero confidence to
   63 at full confidence. This adds an explicit anger-confidence interaction.

## Evidence check

Direct forward passes confirm that each candidate matches all 32 labels.
Each changes the 16 original positive decisions that must become negative
and preserves the other 16 decisions. The smallest signed margins are:

| Candidate | Matching labels | Minimum signed margin |
| --- | --- | --- |
| Input re-interpretation | 32/32 | 1.051715 |
| Output shift | 32/32 | 1.086301 |
| Interaction | 32/32 | 0.417839 |

A signed margin is `g(x)` for label 1 and `-g(x)` for label 0.
The constants above define hand-written hypotheses. No training or fitting
loop was used.

## Selected candidate

**Choose candidate 1: ignore anger.** It explains every label through one
input change, without additional thresholds or penalty coefficients.
Candidates 2 and 3 also fit the evidence, so the labels do not establish
that candidate 1 is the intended rule. The selection rests on simplicity.

The candidates differ outside the examples. Candidate 1 removes all
dependence on the supplied anger value. Candidate 2 retains that dependence
and adds a threshold change. Candidate 3 retains the model's anger response
and adds a penalty that depends on confidence.

No model was edited. No query file was created.
