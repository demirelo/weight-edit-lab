# Candidate rules for step 2

Let `f(x)` be the unchanged `model_in.json` logit. Escalate when the candidate logit is greater than zero. Rows below use one-based data-row numbers, excluding the CSV header.

All three candidates match **32/32 current labels** in `evidence.csv`, including the 16 changed cases and 16 unchanged cases. These are distinct hypotheses, not established rules.

## A. Output shift — EU bonus (selected)

Use `g(x) = f(x) + 20 * region_eu`.

EU alerts receive a 20-point logit bonus. Other alerts retain their current logit. The changed examples have logits from approximately -18.578 to -0.604. The nearest suppressed EU example has logit approximately -39.570. Thus 20 separates the supplied cases.

**Why select A:** It explains every current label with one feature and one constant. The evidence does not identify the constant exactly: any bonus strictly above 18.57799742277407 and at most 39.57044146014843 matches the current examples. Select 20 as a simple hypothesis within that interval.

## B. Region override — raw-feature box

Force escalation when all conditions hold:

- `region_eu = 1`
- `urgency >= 0.20`
- `retry_count <= 0.95`
- `latency_spike >= 0.20`
- `error_rate <= 0.95`

Otherwise, retain `f(x)` and its decision. This box contains every changed example and no currently labelled negative example. It has weaker support because it needs several independent conditions.

## C. Interaction — impact and urgency compensate

For EU alerts, force escalation when `impact + urgency >= 0.95`. Otherwise, retain `f(x)` and its decision.

This rule makes the required urgency depend on impact: `urgency >= 0.95 - impact`. Every changed example meets this condition. Every currently labelled negative EU example falls below it. This rule forces escalation regardless of the current logit when the threshold is met; A instead requires the current logit to exceed -20.

## Earlier correction and historical labels

The inferred earlier correction is that **tone_anger must not affect escalation**. Every first-layer weight from `tone_anger` is zero. The current model also matches all 32 step-1 labels. Each candidate retains this independence because its added conditions omit tone_anger.

TASK.md permits later corrections to override historical labels. Relative to `evidence_step1.csv`, A changes rows 2 and 6; B changes rows 2 and 7; C changes rows 2, 6, 7, and 10. Each difference occurs inside that candidate's proposed correction region. No step-2 labels exist for those historical inputs, so their new labels remain unverified.

Only forward-pass checks were used. No model weights were changed. No query file was created because the query allowance is zero.
