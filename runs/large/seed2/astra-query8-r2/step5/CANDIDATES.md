# Candidate rules for step 5

These are hypotheses, not confirmed rules. No weights have been changed.
Rows below use one-based data-row numbers, excluding the CSV header.

## Evidence and baseline uncertainty

All first 16 examples have `maintenance_window = 1`,
`users_affected < 0.42`, and label 0. Maintenance examples 21 and 28
have more than 0.53 users affected and label 1. This supports a maintenance
suppression rule, but does not establish its cutoff or treatment of critical tiers.

A maintenance-only override of `model_in.json` cannot match all current labels:
row 18 has users affected 0.5523 and changes from 1 to 0; row 19 has no
maintenance and changes from 1 to 0; row 22 has no maintenance and changes
from 0 to 1. Earlier files contain labels from their respective steps;
later corrections can override them. They do not resolve these three differences.

To give complete, testable candidates, each candidate starts with the current
model's decision and applies these two **provisional shared conditions**, in order:

1. Set the label to 0 when `confidence < 0.4`, `impact < 0.2`,
   `urgency < 0.75`, `error_rate < 0.5`, and `tier_critical = 0`.
2. Set the label to 1 when `confidence < 0.4`, `error_rate > 0.75`,
   and `users_affected > 0.5`.

The first condition explains rows 18 and 19. The second explains row 22
and retains row 21. These conditions are not uniquely supported by the evidence;
they could reflect errors in earlier edits rather than the intended new rule.
Queries 6–8 test their generalization. No historical rule is asserted as confirmed.

## Four distinct candidates

After the shared conditions, apply the following final override. Retain the
result from the shared conditions everywhere outside the override.

| Candidate | Set the label to 0 when |
| --- | --- |
| A | `maintenance_window = 1` and `users_affected < 0.45` |
| B | `maintenance_window = 1` and `users_affected < 0.50` |
| C | `maintenance_window = 1` and `users_affected <= 0.50` |
| D | `maintenance_window = 1` and either (`tier_critical = 0` and `users_affected < 0.45`) or (`tier_critical = 1` and `users_affected < 0.60`) |

Direct forward-pass checks confirm that each complete candidate matches all
32 current labels. This check does not establish that any candidate is correct
outside those examples. No training, fitting, or weight edits were used.

## Query predictions

`query.csv` contains eight inputs. Each row has a verified positive current-model
decision except row 8, whose current-model decision is 0.

| Query | Purpose | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | Test users affected exactly 0.45 during maintenance | 1 | 0 | 0 | 1 |
| 2 | Test users affected 0.475 during maintenance | 1 | 0 | 0 | 1 |
| 3 | Test users affected exactly 0.50 during maintenance | 1 | 1 | 0 | 1 |
| 4 | Test users affected 0.5001 during maintenance | 1 | 1 | 1 | 1 |
| 5 | Test critical tier with users affected 0.55 during maintenance | 1 | 1 | 1 | 0 |
| 6 | Test shared suppression at urgency 0.70 | 0 | 0 | 0 | 0 |
| 7 | Test the same input at urgency 0.76 | 1 | 1 | 1 | 1 |
| 8 | Test shared escalation with high error rate and moderate user impact | 1 | 1 | 1 | 1 |

Queries 1, 3, and 5 distinguish all four candidates. The other queries test
the cutoff neighborhood and the shared assumptions. If answers reject all
four candidates, revise the hypotheses before editing the model.
