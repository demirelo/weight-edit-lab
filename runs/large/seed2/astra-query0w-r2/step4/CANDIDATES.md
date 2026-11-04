# Candidate rules for step 4

Let `f(x)` be the unchanged logit from `model_in.json`. Escalate when the candidate logit is greater than zero.

The current model suppresses rows 1–16, but their new labels require escalation. All have `confidence < 0.4`. Low confidence alone is insufficient: rows 17, 22, 24–26, 29, and 30 have low confidence and must stay suppressed.

Define a proposed region `G` by `confidence < 0.4` and at least one of these conditions:

- `impact > 0.85`.
- `urgency > 0.65`.
- `impact > 0.7` and `urgency > 0.3`.
- `users_affected > 0.7` and `urgency > 0.5`.

Unspecified features have their full permitted ranges. Thus, `G` is a union of four boxes in raw feature space. These thresholds are hypotheses, not established boundaries.

1. **Output shift.** Use `f(x) + 1.6` inside `G`; use `f(x)` elsewhere. A finite bonus can leave sufficiently negative logits suppressed.

2. **Region override.** Use logit `1` inside `G`; use `f(x)` elsewhere. Low confidence together with one of the severity conditions forces escalation, regardless of the previous logit.

3. **Input re-interpretation.** Inside `G`, set both `impact` and `urgency` to `1`, then evaluate the unchanged model. Keep all other inputs unchanged. Outside `G`, evaluate the original input. This treats those two severity readings as maximum values when the region condition holds. The model still determines the resulting decision.

4. **Interaction.** Use `f(x) + 1.2 + urgency` inside `G`; use `f(x)` elsewhere. Urgency has an additional positive effect only when low confidence and a severity condition activate the correction.

Forward-pass checks confirm that each candidate matches **32/32** labels in `evidence.csv`: all 16 changed labels and all 16 unchanged labels. No training, fitting loop, or weight edit was used. The candidates specify different behavior beyond these examples; equal example accuracy does not establish equal behavior over the full input domain.

**Provisional selection: candidate 2, region override.** The changed examples span current logits from approximately -1.562 to -0.050, yet all require escalation. A region override explains this without choosing a bonus size or replacement input values. Its four-box boundary remains weakly supported; the evidence does not prove that this is the intended rule.

The existing model ignores `tone_anger`, adds an EU bonus of 20 before its final maximum operation, and implements `max(previous_logit, error_rate + tier_critical - 1.7)`. These operations support the earlier corrections: ignore anger, give EU alerts a logit bonus, and force escalation for critical-tier alerts with `error_rate > 0.7`. The proposed region does not depend on anger. Candidates 1, 2, and 4 only add escalation decisions, so they preserve existing positive decisions. Candidate 3 retains the critical-tier/error-rate condition but needs broader checks for other preservation requirements.

Earlier CSV labels describe earlier steps. They are not additional immutable step-4 labels: later corrections may override them, as TASK.md states. Historical behavior outside the proposed region remains exactly that of the supplied model for all four candidates.

No queries were requested. No model file was changed.
