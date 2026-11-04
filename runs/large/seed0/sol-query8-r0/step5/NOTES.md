# Inferred rules and edit

The retained weights and earlier evidence indicate these prior corrections:

1. Ignore `tone_anger`.
2. Apply a +18 EU adjustment to the underlying logit, before later overrides.
3. Escalate critical-tier alerts when `error_rate > 0.70`.
4. Escalate outside maintenance when `confidence < 0.40`, `urgency > 0.20`, and `impact + 1.2*urgency + 0.8*error_rate > 1.12`.

The new rule suppresses escalation when `maintenance_window == 1` and `users_affected <= 0.50`. It takes precedence over prior escalation rules. The query answers include equality and exclude a service-age restriction. This revises candidate B's strict comparison.

I retained the existing computations and added a ReLU gate. Let `z` be the input-model logit and `g = ReLU(users_affected - 0.50) + (1 - maintenance_window)`. The new logit is `min(ReLU(z), g) - ReLU(-z)`. Thus, suppression gives a nonpositive logit; elsewhere, its sign decision matches the input model. Positive logit magnitudes can change. Two equivalent minimum formulas protect small positive values from cancellation.

Validation passed: 32 evidence labels, eight query labels, 50,000 random inputs, 360 boundary inputs, and prior-evidence decision preservation outside suppression. No training or fitting was used.
