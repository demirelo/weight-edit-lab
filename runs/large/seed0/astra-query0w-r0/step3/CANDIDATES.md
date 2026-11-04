# Candidate rules for step 3

Let `z(x)` be the unchanged logit from `model_in.json`. Let `t` mean
`tier_critical` and `e` mean `error_rate`. Define region `R` by
`t = 1` and `e > 0.70`. Escalate when the candidate logit is positive.

1. **Region override — selected.** Force escalation in `R`. Keep the current
   decision elsewhere. A decision-level formula is `z1 = 1` in `R`, and
   `z1 = z(x)` elsewhere. This rule treats high error rates on critical tiers
   as sufficient for escalation, regardless of the other features.

2. **Output shift.** Add a fixed bonus of 90 in `R`: `z2 = z(x) + 90` in
   `R`, and `z2 = z(x)` elsewhere. This rule can still suppress an alert in
   `R` if its original logit is at most -90.

3. **Interaction.** Add a bonus that grows with the error rate only for a
   critical tier: `z3 = z(x) + 2000*t*max(e - 0.70, 0)`. This rule keeps the
   original logit outside `R`. Inside `R`, the result depends on both the
   original logit and the distance above the threshold.

## Evidence and selection

Forward checks confirm that each candidate matches **32/32 labels in
`evidence.csv`**. Each changes all 16 required decisions and keeps all 16
near-miss decisions. The 16 changed rows have `t = 1`, error rates from
0.739 to 0.998, and original logits from about -85.942 to -4.549.
The constants above were chosen by hand; no training or fitting was used.

**Select candidate 1.** The changed cases span widely different original
logits. Their common critical-tier and high-error condition supports a
direct escalation rule. The examples do not establish the exact threshold
or distinguish an override from the two bonus rules. Treat 0.70 as a
hypothesis, not a confirmed boundary.

The candidates make different predictions on valid constructed inputs:

| Input; all unlisted features are zero | Original logit | Override | Fixed bonus | Interaction |
| --- | ---: | --- | --- | --- |
| `t=1, e=0.701` | -98.106 | Escalate | Suppress | Suppress |
| `t=1, e=0.74, confidence=1, dup_alerts=1` | -89.841 | Escalate | Escalate | Suppress |

These are forward-check examples, not requests for labels.

## Earlier evidence

All three candidates also match **32/32 step-2 labels**. They match
**30/32 step-1 labels**. Step-1 data rows 8 and 9 already disagree with the
current model and lie outside `R`: their current logits are approximately
2.858 and -1.077, but their recorded labels are 0 and 1. Thus these candidates
are consistent with all current-step labels, but not every historical label.
Keeping the current model unchanged outside `R` preserves those two
existing discrepancies. The available evidence does not establish their cause.

No model weights were changed. No query file was created.
