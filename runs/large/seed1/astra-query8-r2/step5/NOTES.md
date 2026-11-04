I made no training or fitted-weight updates.

Earlier inferred corrections:
1. Ignore tone_anger; its input weights are zero.
2. Remove the EU penalty; the existing model adds 20 to the EU logit.
3. Escalate critical-tier alerts when error_rate > 0.70.
4. Add escalation when confidence < 0.40 and urgency > 0.60, or when confidence < 0.40, impact > 0.675, and users_affected > 0.45. These impact/users thresholds describe the inherited implementation, not uniquely established rules.

New inference: maintenance suppresses alerts with users_affected <= 0.50. Answers reject all four candidates, including their urgency and EU branches. The exact threshold remains uncertain: 0.50 is suppressed; 0.5999 is allowed.

Evidence row 18 also requires suppression above this threshold. I infer that the low-confidence impact/users branch applies only outside maintenance. This preserves all step-4 examples before applying the new suppression. Other explanations remain possible.

I retained existing weights except for that branch gate and added a ReLU minimum gate. It preserves decisions outside suppression. A bounded steep slope preserves logits except within 0.000001 above the users threshold.

Checks: all 40 current evidence/query labels pass; 50,000 random forward passes match the implemented rule. Hidden-test accuracy is unverified.
