# Step 4 candidates

These are hypotheses, not confirmed rules. Each matches all 32 labels in
`evidence.csv`. Forward passes checked the rules; no training or fitting was used.

Let `F(x)` be the current model logit. Escalate when the proposed logit is greater
than zero. Let `i`, `u`, and `c` denote impact, urgency, and confidence.

The current model has a useful exact decomposition:

`F(x) = max(S(x), 0) + T(x)`

Here, `S(x)` is the pre-activation of unit 0 in the penultimate layer, and
`T(x) = tier_critical * max(error_rate - 0.7, 0)`.

## Candidate 1: Region override

Force escalation within either raw-feature box:

- `c < 0.4` and `u >= 0.6`.
- `c < 0.4`, `i >= 0.45`, and `u >= 0.2`.

Use logit `max(F(x), 1)` inside this union. Use `F(x)` elsewhere.
All unlisted features are unrestricted. This rule uses two boxes, not a box
around each example. It matches 32/32 current labels, but its separate thresholds
have limited support.

## Candidate 2: Input re-interpretation

When `c < 0.4`, replace impact with `min(i + 0.6*u, 1)` and apply the current
model to that input. Otherwise, apply the current model without an input change.
Keep every other input unchanged.

This rule treats urgency as additional impact when confidence is low. It matches
32/32 current labels. The coefficient 0.6 is a hypothesis; the examples do not
establish it as an exact value.

## Candidate 3: Interaction

Use the logit:

`G(x) = max(S(x) + 80*u*I(c < 0.4), 0) + T(x)`

`I(condition)` is 1 when the condition holds and 0 otherwise. Low confidence
thus adds an urgency-dependent bonus to the internal score, before its ReLU.
This is not an unconditional bonus to the already clipped output `F(x)`.

This rule matches 32/32 current labels. It preserves the existing critical-tier
term and leaves the model unchanged when `c >= 0.4`.

## Provisional choice

Choose Candidate 3. It explains why low confidence can change a suppressed case
to escalation, while low urgency or a sufficiently negative internal score still
prevents escalation. It uses one confidence condition and one urgency term.
The choice is provisional: the labels cannot distinguish these three rules or
determine the exact threshold and coefficient. No queries are allowed in this phase.

## Historical evidence check

The historical files contain labels from earlier steps. TASK.md permits later
corrections to override those labels. Therefore, agreement with all historical
labels is not claimed:

| Evidence file | Current model | Candidate 1 | Candidate 2 | Candidate 3 |
| --- | ---: | ---: | ---: | ---: |
| evidence.csv | 16/32 | 32/32 | 32/32 | 32/32 |
| evidence_step1.csv | 30/32 | 26/32 | 27/32 | 27/32 |
| evidence_step2.csv | 32/32 | 30/32 | 29/32 | 29/32 |
| evidence_step3.csv | 32/32 | 32/32 | 32/32 | 32/32 |

These differences remain unresolved without later labels for the historical
inputs. The current model itself already disagrees with two step-1 labels.
All three candidates retain independence from tone_anger and retain escalation
when tier_critical is 1 and error_rate exceeds 0.7. No model edit was made.
