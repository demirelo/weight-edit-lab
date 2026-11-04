# Candidate rules for step 5

These are hypotheses, not confirmed rules. Each candidate reproduces all 32 labels in evidence.csv when applied to model_in.json. Forward passes confirm this; no weights were changed or fitted.

Let B be the current model decision (logit > 0). Apply each veto first, then its promotion condition. Otherwise retain B. All comparisons below are exact.

## A: User threshold 0.45, with a separate urgency veto

- Veto escalation when maintenance_window = 1 and either users_affected < 0.45 or urgency < 0.10.
- Force escalation when maintenance_window = 0, confidence < 0.05, urgency >= 0.60, and users_affected >= 0.50.

## B: User threshold 0.50, with an impact condition on the urgency veto

- Veto escalation when maintenance_window = 1 and either users_affected < 0.50 or both impact < 0.60 and urgency < 0.10.
- Use the same promotion condition as A.

## C: User threshold 0.45, with promotion based on error rate

- Use the same veto as A.
- Force escalation when maintenance_window = 0, confidence < 0.05, error_rate >= 0.75, and users_affected >= 0.50.

## Evidence limits

A maintenance veto based only on users_affected cannot reproduce all labels. Evidence row 22 requires escalation outside maintenance despite B = 0. Evidence row 29 requires suppression during maintenance despite users_affected = 0.8177 and B = 1. The secondary clauses above explain these observations, but the evidence does not establish their scope. They may instead indicate errors in an earlier correction. The queries test these uncertainties without assuming label noise.

Earlier evidence records labels at earlier steps. A later correction can override them. These candidates retain B except where their stated clauses apply.

## Query predictions

Rows follow query.csv order. Values are hypothetical labels.

| Row | Test | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | users_affected = 0.4499 during maintenance | 0 | 0 | 0 |
| 2 | users_affected = 0.45 during maintenance | 1 | 0 | 1 |
| 3 | users_affected = 0.475 during maintenance | 1 | 0 | 1 |
| 4 | users_affected = 0.4999 during maintenance | 1 | 0 | 1 |
| 5 | users_affected = 0.50 during maintenance | 1 | 1 | 1 |
| 6 | High impact, low urgency, and many users during maintenance | 0 | 1 | 0 |
| 7 | Low confidence and high error rate; urgency = 0.55 | 0 | 0 | 1 |
| 8 | Low confidence and urgency = 0.70; error_rate = 0.50 | 1 | 1 | 0 |

Rows 1 and 5 check the proposed threshold bounds. Rows 2-4 distinguish the thresholds. Row 6 tests the urgency veto. Rows 7-8 test the promotion condition.
