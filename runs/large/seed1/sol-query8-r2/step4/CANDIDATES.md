# Candidate rules for step 4

Let `B(x)` mean that `model_in.json` gives a logit greater than zero. Each candidate gives the label `B(x) OR R(x)`. Thus, each candidate keeps existing escalations and adds escalations where its rule applies. All four candidates match all 32 labels in `evidence.csv`. Earlier evidence describes earlier steps; later corrections can override those labels.

Use `i = impact`, `u = urgency`, `n = users_affected`, and `c = confidence`. The thresholds below are hypotheses. The examples do not establish their exact values or boundary conditions.

1. **Separate impact and user thresholds:** `R = (c < 0.4) AND ((u > 0.6) OR ((i > 0.6) AND (n > 0.4)))`.
2. **Weighted impact and user score:** `R = (c < 0.4) AND ((u > 0.6) OR (i + 0.5*n > 0.9))`.
3. **Impact and user product:** `R = (c < 0.4) AND ((u > 0.6) OR (i*n > 0.33))`.
4. **Higher confidence limit:** `R = (c < 0.425) AND ((u > 0.6) OR ((i > 0.6) AND (n > 0.4)))`.

## Query design

All eight query inputs give label 0 in the input model. Features outside the four variables above stay fixed. Binary features are zero; other fixed features are 0.5.

| Query row | Purpose | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 |
|---|---|---|---|---|---|
| 1 | Test just above both separate thresholds | 1 | 0 | 0 | 1 |
| 2 | Test just below the impact threshold | 0 | 0 | 0 | 0 |
| 3 | Test the weighted score alone | 0 | 1 | 0 | 0 |
| 4 | Test the product alone | 0 | 0 | 1 | 0 |
| 5 | Test between the confidence limits | 0 | 0 | 0 | 1 |
| 6 | Test below the lower confidence limit | 1 | 1 | 1 | 1 |
| 7 | Test just below the urgency threshold | 0 | 0 | 0 | 0 |
| 8 | Test just below the user threshold | 0 | 0 | 0 | 0 |

Rows 1, 3, 4, and 5 separate the four candidates. The other rows check nearby threshold behavior. No model weights have been changed.
