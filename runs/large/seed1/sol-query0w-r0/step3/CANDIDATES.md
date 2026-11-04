# Candidate rules for step 3

Let `f(x)` be the logit from `model_in.json`. Let `t = tier_critical`
and `e = error_rate`. Escalate when the proposed logit is greater than zero.
All conditions use the recorded feature values. Each rule matches all 32 labels
in `evidence.csv`, as checked with forward passes. No model was edited or trained.

1. **Output shift:** Add 128 to `f(x)` when `t = 1` and `e >= 0.700`.
   Otherwise, keep `f(x)`. This finite bonus changes all 16 negative logits
   that need escalation. Their lowest current logit is about -116.861.
   A sufficiently negative logit could still cause suppression in this region.

2. **Region override — selected:** Force escalation when `t = 1` and
   `e >= 0.700`, for all values of the other features. Otherwise, keep the
   current decision. For a precise candidate logit, use `max(f(x), 1)` inside
   this region and `f(x)` outside it.

3. **Interaction:** Use `f(x) + 2048 * t * max(e - 0.600, 0)`.
   Error rate adds a continuous bonus above 0.600 only for critical-tier alerts.
   This rule can change decisions between 0.600 and 0.700. Its bonus increases
   with error rate, and it does not guarantee escalation for every current logit.

## Selection and uncertainty

Candidate 2 has the strongest support. All 16 changed examples have `t = 1`
and `e >= 0.700`, despite large differences in their current negative logits.
The rule also preserves all 16 near-miss labels, including noncritical alerts
with high error rates and critical alerts with lower error rates. Two positive
examples have `e = 0.700`.

The labels do not prove the exact threshold or distinguish a forced decision
from a finite bonus. The largest error rate among suppressed critical examples
is 0.594. For the same override form, any threshold in `(0.594, 0.700]` matches
the examples. Candidate 2 uses the simple threshold 0.700 as an inference.
No query inputs were requested or written.
