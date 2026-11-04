I preserved all existing weights and biases and added one independent signal:
`r = ReLU(users_affected - 0.85)`. Identity connections carry this signal
through the existing layers. The former output now passes through ReLU;
a new linear output computes `ReLU(old_logit) + r`.

The new logit is positive exactly when the old logit is positive or
users_affected exceeds 0.85. At or below 0.85, all escalation decisions
remain unchanged, including the threshold itself. Above 0.85, escalation
always occurs, including during startup with low impact. Tone remains
irrelevant because its weights remain zero.

Negative old logits become zero; this preserves the specified decision
rule, which requires a strictly positive logit. Existing positive logits
remain unchanged when the override does not apply.

I used the feature order in model_in.json, model.py, and evidence.csv:
impact, urgency, users_affected, tone_anger, startup_phase, confidence.
All added weights and biases follow directly from this construction.
No training, fitting, or optimization was used.
