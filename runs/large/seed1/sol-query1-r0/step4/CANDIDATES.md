# Candidate rules for step 4

Let `base(x) = 1` when the unchanged `model_in.json` logit is greater than zero; otherwise, let `base(x) = 0`.

Each candidate forces escalation when its condition is true. Otherwise, it keeps `base(x)`. Both candidates match all 32 labels in `evidence.csv`, as checked with forward passes. The examples do not establish the exact thresholds or which candidate is correct.

## Candidate A: User count qualifies high impact

Force escalation when:

```text
confidence < 0.4
AND (
    urgency > 0.6
    OR (impact > 0.6 AND users_affected > 0.4)
)
```

This rule treats high urgency as sufficient. High impact also qualifies when the affected user count is high, even when the error rate is low.

## Candidate B: Error rate qualifies high impact

Force escalation when:

```text
confidence < 0.4
AND (
    urgency > 0.6
    OR (impact > 0.6 AND error_rate > 0.2)
)
```

This rule treats high urgency as sufficient. High impact also qualifies when the error rate is elevated, regardless of the affected user count.

## Query

The query uses low confidence, low urgency, high impact, a high affected user count, and a low error rate. It sets `tier_critical` and `region_eu` to zero to avoid the earlier escalation conditions associated with these features.

The unchanged model returns approximately `-63.086473`, so its label is zero.

| Candidate | Query label | Reason |
| --- | --- | --- |
| A | 1 | High impact and affected user count satisfy the condition. |
| B | 0 | Low urgency and error rate do not satisfy the condition. |

One binary answer separates these two candidates. It does not establish a unique rule among all possible rules. No model weights were changed.
