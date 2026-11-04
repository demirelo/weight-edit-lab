# Candidate rules for step 5

Let L(x) be the unchanged model_in.json logit. Let M be maintenance_window,
U be users_affected, and Q be urgency. Define region R by M = 1 and U < 0.5.
Escalate means the proposed logit is strictly greater than zero.

1. **A: Region override.** Suppress every alert in R. Use L(x) outside R.
   A representative logit inside R is min(L(x), 0).
2. **B: Output shift.** Subtract 80 from L(x) inside R. Use L(x) outside R.
   A sufficiently large original logit can still trigger escalation.
3. **C: Interaction.** Subtract 100 times Q from L(x) inside R. Use L(x)
   outside R. Maintenance changes the effect of urgency when U is below 0.5.
   The extra penalty is zero at Q = 0 and increases with Q.

These are hypotheses, not confirmed rules. The constants are explicit candidate
values, not identified parameters. Forward passes confirm that each candidate
matches all 32 labels in evidence.csv. Rows 1-16 change from escalate to suppress;
rows 17-32 keep their current labels. Every changed row is in R.

The historical files contain labels from earlier steps. Later corrections can
override them, as TASK.md states. These candidates use the current model as the
baseline and preserve its exact logit outside R. They do not assume that all
historical labels remain valid after step 5.

## Query predictions

The first two queries separate all three rule types. Query 3 supplies another
separation. Queries 4-6 test the proposed strict boundary at U = 0.5. Query 7
tests the maintenance condition. Query 8 tests agreement below that boundary.
The predictions below are hypotheses; they are not oracle answers.

| CSV row | U | Q | M | Current logit | A | B | C |
|---|---|---|---|---|---|---|---|
| 1 | 0.49 | 1 | 1 | 91.263616 | 0 | 1 | 0 |
| 2 | 0.25 | 0 | 1 | 30.248280 | 0 | 0 | 1 |
| 3 | 0.49 | 0.8 | 1 | 83.107629 | 0 | 1 | 1 |
| 4 | 0.499 | 1 | 1 | 91.790796 | 0 | 1 | 0 |
| 5 | 0.5 | 1 | 1 | 91.849372 | 1 | 1 | 1 |
| 6 | 0.501 | 1 | 1 | 91.907948 | 1 | 1 | 1 |
| 7 | 0.49 | 1 | 0 | 89.865127 | 1 | 1 | 1 |
| 8 | 0.25 | 1 | 1 | 78.052959 | 0 | 0 | 0 |
