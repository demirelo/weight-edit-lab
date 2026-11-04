# Candidate rules for step 4

All four candidates match all 32 labels in `evidence.csv`, as checked by forward passes. These are hypotheses, not confirmed rules. Earlier evidence files contain labels from earlier steps; the task permits later corrections to override those labels.

Let `F(x)` be the current model logit. Let `c`, `u`, `i`, and `v` denote confidence, urgency, impact, and users_affected. Each candidate uses the proposed condition `c < 0.4`. The evidence does not establish this exact threshold.

## A. Double urgency at low confidence

**Kind: Input re-interpretation.** If `c < 0.4`, return `F(x)` with urgency replaced by `2*u`. Otherwise, return `F(x)`. Do not cap the modified urgency at 1. Keep all other inputs unchanged.

## B. Escalate in two raw-feature boxes

**Kind: Region override.** Force escalation if either box applies:

- `c < 0.4` and `u > 0.6`.
- `c < 0.4`, `i > 0.65`, and `v > 0.45`.

Outside these boxes, retain the current decision. A concrete logit is `max(F(x), 1)` inside the boxes and `F(x)` outside them. This rule makes escalation independent of the remaining features inside either box.

## C. Add a confidence-gated urgency contribution

**Kind: Interaction.** The current network computes `F(x) = ReLU(S(x)) + ReLU(H(x))`. Here, `S` and `H` are the two coordinates before the ReLU in the penultimate layer, in file order. Keep `H` unchanged. If `c < 0.4`, return `ReLU(S(x) + 90*u) + ReLU(H(x))`. Otherwise, return `F(x)`.

Confidence therefore controls an extra linear urgency contribution to the existing score. This differs from A, which changes the input to all downstream nonlinear units. The hand-chosen coefficient 90 is not uniquely determined: coefficients 80 and 100 also match the 32 labels.

## D. Transfer urgency into impact at low confidence

**Kind: Input re-interpretation.** If `c < 0.4`, return `F(x)` with impact replaced by `i + u`. Otherwise, return `F(x)`. Do not cap the modified impact at 1. Keep urgency and all other inputs unchanged.

## Query predictions

Rows refer to data rows in `query.csv`. A prediction of 1 means escalate; 0 means suppress. These are candidate predictions, not oracle labels.

| Row | A | B | C | D | Purpose |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 0 | Separate the raw-feature override from score-dependent rules. |
| 2 | 0 | 0 | 0 | 1 | Separate transfer into impact from the other rules. |
| 3 | 0 | 0 | 1 | 1 | Separate the linear interaction from urgency re-interpretation. |
| 4 | 1 | 0 | 1 | 1 | Check urgency re-interpretation outside the override boxes. |
| 5 | 1 | 1 | 1 | 1 | Test confidence just below 0.4. |
| 6 | 0 | 0 | 0 | 0 | Test confidence exactly at 0.4. |
| 7 | 0 | 0 | 0 | 0 | Test confidence just above 0.4. |
| 8 | 1 | 1 | 1 | 1 | Test modified inputs above 1; capped urgency in A predicts 0. |

The first four rows give each candidate a distinct prediction sequence. Rows 5–7 differ only in confidence. All query inputs satisfy the raw input bounds. No model weights were changed.
