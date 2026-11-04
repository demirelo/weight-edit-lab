# Candidate rules for step 3

Let `f(x)` be the unchanged logit from `model_in.json`. Let `t` be
`tier_critical`, and let `e` be `error_rate`. Escalate when the proposed
logit is greater than zero. All three candidates keep `f(x)` outside
`R = {t = 1 and e > 0.70}`.

1. **Region override:** Force escalation inside R. Use `f(x)` elsewhere.
2. **Output shift:** Use `f(x) + 80` inside R. Use `f(x)` elsewhere.
   A sufficiently negative original logit can still suppress escalation.
3. **Interaction:** Use `f(x) + 1500 * t * max(e - 0.70, 0)`.
   Error rate adds an increasing bonus only for a critical tier. A point
   just above the threshold can still fail to escalate.

The constants are explicit hypotheses, not identified parameters. No
training, optimization, or parameter search was used.

## Evidence check

Each candidate matches all 32 current labels. Rows 1–16 change from
suppression to escalation. All have a critical tier and error rates from
0.731261 to 0.986801. Rows 17–32 retain their labels. The largest error
rate among critical-tier negative examples is 0.653966. Noncritical
negative examples include error rates above 0.95.

Each candidate also matches all 32 step-2 labels. Each retains the current
model's decisions on all step-1 examples. Two historical step-1 labels
(rows 2 and 6) were superseded by step 2: their current logits are
5.842739 and 4.434552; removing the existing EU bonus of 20 makes both
negative and recovers every step-1 label.

The existing model ignores `tone_anger` and adds 20 to EU-region logits.
These support the inferred earlier corrections: remove anger's effect,
then add an EU bonus. All candidates start from this corrected model.

Forward checks on 20,000 constructed random inputs confirmed that the
three candidates make distinct decisions. Those inputs have no supplied
labels, so this check establishes differences, not correctness.

## Selected candidate

**Select candidate 1: force escalation when `tier_critical = 1` and
`error_rate > 0.70`.** It gives a simple explanation for all 16 changed
cases, despite original logits from -71.770707 to -2.764020. It also
explains the unchanged noncritical cases with high error rates.

The evidence does not prove an override instead of a bonus. It also does
not identify the exact threshold or equality rule. For the strict
comparison above, any threshold from 0.6539663462217735 inclusive to
0.7312610300010263 exclusive fits the current labels. The value 0.70 is
a proposed boundary within that interval.

No model was edited. No query file was created.
