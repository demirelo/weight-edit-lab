# Candidate rules

Let `f(x)` be the current model logit. Let `t = tier_critical`,
`e = error_rate`, and `R = (t = 1 and e > 0.70)`.
Escalate when the candidate logit is greater than zero.

All four candidates match all 32 labels in `evidence.csv`. Each leaves the
current model unchanged outside R. The examples suggest a critical-tier,
high-error condition, but they do not establish its threshold or mechanism.
The value 0.70 is a hypothesis.

1. **A — Region override.** Force escalation inside R. Else use `f(x) > 0`.
2. **B — Output shift.** Use `f(x) + 80` inside R. Else use `f(x)`.
   A fixed bonus can leave very negative logits below zero.
3. **C — Input re-interpretation.** Inside R, evaluate the current model with
   `impact` replaced by `impact + 1`. Keep every other input unchanged.
   Do not clip the modified impact; this hypothesis uses a shifted internal
   scale. Query inputs themselves remain within the required range.
   Outside R, evaluate the original inputs.
4. **D — Interaction.** Use `f(x) + 1600 * t * max(e - 0.70, 0)`.
   Critical tier enables a bonus that increases with excess error rate.
   Noncritical tier disables this bonus.

These are candidate rules, not established corrections. Constants come from
explicit hypotheses and forward-pass checks; no weights were trained or edited.

All candidates also match all 40 step-2 labels. Each retains the current
model's two disagreements with step-1 labels (data rows 2 and 6). Neither
row lies in R. These historical disagreements already exist in `model_in.json`;
they are not introduced by these candidates. TASK.md permits later corrections
to supersede earlier labels.

# Query design

Rows refer to data rows in `query.csv`. Entries below are candidate predictions,
not supplied answers. All omitted feature values in the descriptions remain
as recorded in the CSV.

| Row | Purpose | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | Separate fixed bonus/input shift from override/error interaction | 1 | 0 | 0 | 1 |
| 2 | Separate input shift from fixed bonus | 1 | 0 | 1 | 1 |
| 3 | Separate override from all finite corrections at low excess error | 1 | 0 | 0 | 0 |
| 4 | Separate fixed bonus from the increasing error bonus | 1 | 1 | 1 | 0 |
| 5 | Test error rate 0.699 below the proposed threshold | 0 | 0 | 0 | 0 |
| 6 | Test error rate 0.700 at the proposed threshold | 0 | 0 | 0 | 0 |
| 7 | Test error rate 0.701 above the proposed threshold | 1 | 1 | 1 | 0 |
| 8 | Repeat row 1 with noncritical tier to test the tier condition | 0 | 0 | 0 | 0 |

The first four rows distinguish the mechanisms. Rows 5–7 share every input
except error rate and test the boundary. Row 8 tests the common tier condition.
Answers that match no column will require a revised hypothesis.
