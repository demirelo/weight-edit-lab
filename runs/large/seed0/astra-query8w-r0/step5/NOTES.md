Inferred new rule: suppress escalation when maintenance_window = 1 and users_affected <= 0.5. Keep the current decision elsewhere. Query row 3 includes the boundary; row 4 excludes 0.51. This revises candidate B and rejects A, C, and D.

Earlier corrections inferred from historical evidence and retained weights:
1. Ignore tone_anger.
2. Compensate the EU-region penalty with a +16.33 logit adjustment.
3. Allow escalation for critical-tier alerts when error_rate > 0.7.
4. Allow extra escalation from doubled urgency when confidence < 0.4 outside maintenance.

I retained all original computations and added a ReLU gate. Let f be the original nonnegative logit and g = 2048*(ReLU(users_affected - 0.5) + 1 - maintenance_window). The output is f - ReLU(f - g), or min(f,g). It is zero throughout the suppression region and preserves the decision elsewhere. Outside maintenance, it also preserves the logit: interval arithmetic bounds f below 1161. Maintenance logits above the users threshold can decrease without changing their sign.

No training or fitting occurred. Checks passed: 32 evidence labels, eight query labels, 160 historical inputs against current-model preservation, 50,000 random inputs, and 100 boundary inputs, including adjacent floats.
