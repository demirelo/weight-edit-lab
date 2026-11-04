# Candidate rules

Let `f(x)` be the original model logit, `a = tone_anger`, and `i = impact`.
Each candidate escalates if and only if its new logit `g(x) > 0`.
All other inputs retain their supplied values.

## 1. Input re-interpretation — ignore anger

Set `tone_anger` to zero before evaluating the original model:

`g(x) = f(x with tone_anger = 0)`.

Apply this rule to every input. Anger cannot change the decision when the
other features stay fixed.

## 2. Output shift — raise the escalation threshold by anger region

Subtract a constant within each of two raw-input regions:

- When `a <= 0.70`, use `g(x) = f(x) - 40`.
- When `a > 0.70`, use `g(x) = f(x) - 45`.

This rule retains the model's response to anger within each region. It also
changes the decision threshold when anger is zero.

## 3. Interaction — make the anger penalty depend on impact

Use `g(x) = f(x) - a * (66 - 4*i)` for every input.

The correction couples anger and impact. The penalty per unit of anger falls
from 66 at zero impact to 62 at full impact. This rule retains the original
model at zero anger and can retain an anger effect elsewhere.

## Evidence check

Forward passes on all supplied rows give these results. Row numbers exclude
the CSV header. A signed margin is `g(x)` for label 1 and `-g(x)` for label 0.

| Candidate | Correct labels | Smallest signed margin |
| --- | ---: | ---: |
| 1. Input re-interpretation | 32/32 | 1.068771 |
| 2. Output shift | 32/32 | 1.024318 |
| 3. Interaction | 32/32 | 0.209298 |

Each candidate changes rows 1–16 from escalate to suppress. Each preserves
the original decisions on rows 17–32, including all eight escalation labels.
The original model matches 16/32 labels.

## Selected candidate

Choose **candidate 1: ignore `tone_anger`**. Removing this one input explains
every correction and preserves every supplied near-miss label. It requires
no added thresholds or penalty coefficients. Candidates 2 and 3 show that
the labels also permit other rule types; their constants are hypotheses,
not established policy values.

The evidence does not identify a unique rule or establish behavior outside
the supplied examples. This selection is provisional. No training or fitting
was used. No model was edited, and no query file was created.
