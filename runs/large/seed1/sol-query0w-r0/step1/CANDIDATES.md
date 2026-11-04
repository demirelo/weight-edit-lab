# Candidate rules

Let `f(x)` be the original model logit, `a = tone_anger`, and
`c = confidence`. For each candidate, escalate if and only if its new logit
is greater than zero. Keep all unspecified input values unchanged.

## A. Output shift

Subtract a constant penalty in each anger region:

- For `a < 0.8`, use `g(x) = f(x) - 40`.
- For `a >= 0.8`, use `g(x) = f(x) - 45`.

This rule raises the evidence required for escalation. The penalty is larger
in the high-anger region.

## B. Input re-interpretation — selected

Set `tone_anger` to zero before evaluating the original model:

`g(x) = f(x with tone_anger = 0)`.

This rule removes anger from the decision. All other features retain their
original model effects, evaluated with anger set to zero.

## C. Interaction

Apply an anger penalty whose strength depends on confidence:

`g(x) = f(x) - (70 - 10*c)*a`.

At zero confidence, subtract `70*a`. At full confidence, subtract `60*a`.
Thus, higher confidence reduces the added anger penalty.

## Evidence and selection

Forward evaluation confirms that each candidate matches all 32 labels.
Each suppresses rows 1–16, which the original model escalates. Each preserves
the original decisions on rows 17–32: eight escalations and eight suppressions.

| Candidate | Labels matched | Smallest signed logit margin* |
| --- | --- | --- |
| A | 32/32 | 1.024318 |
| B | 32/32 | 1.068771 |
| C | 32/32 | 0.635486 |

*Use `g(x)` for label 1 and `-g(x)` for label 0.

Select **B** as the best-supported rule. It explains every label with one
feature change and needs no new thresholds or penalty coefficients.
Candidates A and C show that the labels do not identify a unique rule.
This selection is an inference, not a confirmed correction.

No model edit or query file is part of this phase.
