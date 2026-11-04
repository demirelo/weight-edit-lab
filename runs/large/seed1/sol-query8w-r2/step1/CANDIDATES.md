# Candidate rules

Let `f(x)` be the unchanged model logit, `a = tone_anger`, and
`c = confidence`. Each candidate escalates exactly when its new logit is
strictly greater than zero. Each candidate matches all 32 evidence labels.
These are hypotheses; the evidence does not establish a unique rule.

1. **Input re-interpretation (A): ignore anger.** Set `tone_anger` to zero
   before the model runs. New logit: `f(x with tone_anger = 0)`.
2. **Output shift (B): raise the escalation threshold.** Subtract 40 from
   the current logit. Subtract another 5 when `tone_anger >= 0.8`.
   New logit: `f(x) - 40 - 5 * indicator(a >= 0.8)`.
3. **Interaction (C): apply an anger penalty that depends on confidence.**
   New logit: `f(x) - 62*a - 4*max(a + c - 1, 0)`.
   The extra anger penalty starts at `a > 1 - c`, so confidence changes
   the effect of anger. This rule uses a ReLU interaction.

The constants define explicit alternatives. They were chosen by reasoning
and checked with forward passes. No model weights were changed or fitted.

## Queries

Each query copies the stated evidence row (numbered from 1, excluding the
header) and changes only `tone_anger`. All other input values stay the same.
Labels below are candidate predictions, not supplied answers.

| Query | Evidence row | tone_anger | A | B | C |
| --- | --- | --- | --- | --- | --- |
| 1 | 19 | 0 | 1 | 0 | 1 |
| 2 | 19 | 1 | 1 | 1 | 0 |
| 3 | 1 | 0.25 | 0 | 0 | 1 |
| 4 | 1 | 1 | 0 | 1 | 0 |
| 5 | 6 | 0.79 | 0 | 1 | 0 |
| 6 | 6 | 0.81 | 0 | 0 | 0 |
| 7 | 30 | 0 | 1 | 0 | 1 |
| 8 | 30 | 1 | 1 | 1 | 0 |

Queries 1-4 distinguish the three kinds of rule. The paired inputs test
whether anger still changes the decision. Queries 5-6 cross the output
shift boundary at 0.8. Queries 7-8 repeat the anger test on a second case
that escalates when anger is zero.
