# Candidate rules for step 4

Let `f(x)` be the unchanged `model_in.json` logit. Let `c`, `u`, and `i` mean confidence, urgency, and impact. Each candidate escalates if its resulting logit is greater than zero. Conditions use strict inequalities as written.

All three candidates match all 32 labels in `evidence.csv`: 16 changed decisions and 16 unchanged decisions. I checked them with forward passes and direct arithmetic. I did not train or edit the model. Earlier evidence files contain labels from earlier steps; a later correction can override those labels.

## 1. Interaction — selected

When `c < 0.4`, urgency adds a bonus to the current logit:

`g(x) = f(x) + 100*u` if `c < 0.4`; otherwise `g(x) = f(x)`.

Confidence controls this additional effect of urgency. Low confidence alone does not force escalation. For example, rows 22 and 26 remain suppressed after the bonus.

## 2. Input re-interpretation

When `c < 0.4`, evaluate the current model with urgency doubled:

`g(x) = f(x with urgency = 2*u)` if `c < 0.4`; otherwise `g(x) = f(x)`.

Do not cap the modified urgency at 1. This candidate can therefore evaluate the model outside the original input range. All other inputs stay unchanged. Capping the doubled urgency at 1 fails six supplied labels, so it is not part of this candidate.

## 3. Output shift

Add a constant bonus inside a region of raw inputs:

`g(x) = f(x) + 60` if `c < 0.4` and (`u > 0.2` or `i > 0.85`); otherwise `g(x) = f(x)`.

This candidate changes the logit by the same amount throughout the specified region. It uses two more feature thresholds than candidate 1.

## Selection and limits

Candidate 1 has the strongest support: it uses one confidence threshold and one urgency coefficient, keeps the original inputs, and explains why low-urgency alerts can remain suppressed. Candidate 2 is also simple but changes every model response to urgency and can exceed the input range. Candidate 3 needs additional region boundaries.

The labels do not establish a unique rule. In particular, they do not prove that the confidence threshold is exactly 0.4 or that the bonus coefficient is exactly 100. These are explicit hypotheses. The candidates make different predictions beyond the supplied examples.

No query rows were requested. I did not create `query.csv` or `model_out.json`.
