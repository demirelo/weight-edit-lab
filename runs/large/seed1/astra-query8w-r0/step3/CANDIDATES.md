# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Let `t` be
`tier_critical` and `e` be `error_rate`. Escalate when the candidate logit
is greater than zero, or when an explicit override requires escalation.

All three candidates match all 32 labels in `evidence.csv`, as checked by
forward passes. These are hypotheses; the examples do not identify a unique
rule. The constants below are hand-chosen, with no training or fitting.

1. **A — Output shift.** Add 120 to `f(x)` when `t = 1` and `e >= 0.700`.
   Otherwise, use `f(x)`. This finite bonus covers the largest negative
   logit among the changed examples, approximately -116.861. It can still
   suppress inputs with more negative logits.
2. **B — Region override.** Force escalation when `t = 1` and
   `e >= 0.700`, with no restriction on the other features. Outside this
   box, use the current decision. This rule does not depend on the logit
   inside the box.
3. **C — Interaction.** Use the logit
   `f(x) + 600 * t * max(e - 0.600, 0)`.
   The critical-service flag enables an additional error-rate effect.
   The bonus grows with error rate instead of switching to a fixed value
   or forcing a decision. It can change decisions below 0.700.

Each candidate uses the current model, which includes the earlier edits.
No model weights have been changed. Agreement with these examples does not
prove behavior on all inputs or determine precedence for every earlier rule.

The first three query rows separate the rule kinds. Rows 4 and 5 bracket
the proposed 0.700 threshold. Row 6 tests the growing interaction bonus
against the finite bonus at a higher error rate. Row numbers exclude the
CSV header. A prediction of 1 means escalate.

| Query row | Current logit | A | B | C | Purpose |
|---|---:|---:|---:|---:|---|
| 1 | -149.761319 | 0 | 1 | 0 | Separate forced escalation from both finite bonuses |
| 2 | -104.665847 | 1 | 1 | 0 | Separate the fixed bonus from the interaction |
| 3 | -1.875821 | 0 | 0 | 1 | Test the interaction below 0.700 |
| 4 | -104.671226 | 0 | 0 | 0 | Check just below 0.700 |
| 5 | -104.660469 | 1 | 1 | 0 | Check just above 0.700 |
| 6 | -145.765189 | 0 | 1 | 1 | Separate the growing bonus from the fixed bonus |
