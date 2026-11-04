# Candidate rules for step 3

Let `f(x)` be the current model's logit. Escalate when the proposed logit
is greater than zero. Define region `R` as `tier_critical = 1` and
`error_rate > 0.70`. Each candidate keeps the current model outside `R`.

1. **Region override.** Force escalation inside `R`, regardless of the
   current logit. For decision checking, use logit `1` inside `R`.
2. **Output shift.** Add a fixed bonus of `100` to `f(x)` inside `R`.
   This rule can still suppress an alert if its current logit is at most
   `-100`; candidate 1 always escalates it.
3. **Input re-interpretation.** Inside `R`, evaluate the current model with
   `impact = 1` and `urgency = 1`. Keep all other input values. This rule
   treats high error rates on the critical tier as maximum impact and
   urgency. The model still determines the decision.

## Evidence and choice

Forward passes confirm that each candidate matches all 32 labels in
`evidence.csv`. The current model disagrees with rows 1-16 and agrees with
rows 17-32. All 16 changed rows have `tier_critical = 1` and error rates
from `0.739` to `0.998`. Critical-tier negative examples have error rates
at most `0.532`. Noncritical negative examples include high error rates.

**Best-supported candidate: 1, region override.** The changed examples
span current logits from approximately `-85.942` to `-4.549`, yet all
require escalation. A mandatory escalation rule explains this pattern
without assuming a numerical bonus or changing impact and urgency.

The examples do not prove this choice. They also do not identify the
exact threshold or its boundary convention. For these candidates, any
threshold from `0.532` inclusive to `0.739` exclusive gives the same labels
with a strict `>` condition. `0.70` is a proposed threshold.

No model weights were changed. No query file was created.
