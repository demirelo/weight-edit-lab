# Candidate rules

These are provisional hypotheses, not confirmed rules. Both match all 32
labels in `evidence.csv`, including the 16 changed cases and 16 near misses.
Earlier evidence records labels at earlier steps; this correction can override
those labels, as TASK.md permits.

Let `B(x)` be the decision from `model_in.json`: escalate when its logit is
greater than zero. Define a provisional severity condition `S(x)` as true
when at least one of these conditions holds:

- `impact > 0.60` and `urgency > 0.30`.
- `urgency > 0.70`.
- `impact > 0.85` and `users_affected > 0.50`.
- `users_affected > 0.70` and `urgency > 0.50`.

1. **Confidence threshold 0.40:** Escalate if `B(x)` is true, or if
   `confidence < 0.40` and `S(x)` is true. Otherwise, retain `B(x)`.
2. **Confidence threshold 0.45:** Escalate if `B(x)` is true, or if
   `confidence < 0.45` and `S(x)` is true. Otherwise, retain `B(x)`.

The examples do not establish the severity condition uniquely. These rules
demonstrate one remaining ambiguity without treating an inferred rule as fact.
Both retain every positive decision from the input model and ignore tone.

## Query

The query has confidence 0.425, impact 0.65, and urgency 0.65. Its input-model
logit is 0, so `B(x)` is false. Its severity condition is true.

| Candidate | Predicted label |
| --- | --- |
| Confidence threshold 0.40 | 0 |
| Confidence threshold 0.45 | 1 |

One binary answer separates these two candidates. It does not establish that
either candidate is the complete intended rule. No weights were changed.
