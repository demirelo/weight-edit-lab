# Candidate rules for step 4

These are hypotheses. The examples do not establish the exact thresholds or conditions.

Let `baseline(x)` be the decision from the unchanged `model_in.json`, including its earlier corrections. Each candidate forces escalation under the condition below and uses `baseline(x)` everywhere else.

## Candidate A: urgency or impact with affected users

Force escalation when `confidence < 0.4` and either:

- `urgency > 0.6`; or
- `impact > 0.65` and `users_affected > 0.45`.

## Candidate B: urgency or impact with errors or many affected users

Force escalation when `confidence < 0.4` and either:

- `urgency > 0.6`; or
- `impact > 0.65` and either `error_rate > 0.6` or `users_affected > 0.75`.

Both candidates match all 32 labels in `evidence.csv`. Earlier evidence retains its step-specific meaning; a later correction can override an earlier label, as TASK.md permits.

## Query

The query has low confidence, high impact, moderate affected users, low urgency, and a low error rate. Its baseline logit is approximately `-61.3373`.

| Candidate | Predicted label |
| --- | --- |
| A | 1 |
| B | 0 |

One binary answer separates these two hypotheses. It does not establish a unique rule among all possible rules.
