I preserved all existing weights and biases and added a separate override path.

Let f be the input model's logit, e be error_rate, and t be tier_critical. The added units compute:

h = ReLU(e - 0.7)
n = ReLU(1 - t)
q = ReLU(h - n)
output = ReLU(f) + q

For binary t and e in [0, 1], h is at most 0.3. Thus q is zero for noncritical alerts. For critical alerts, q is positive exactly when e > 0.7. The output is positive exactly when the original model escalates or the new rule applies. At e = 0.7, the original escalation decision remains unchanged.

The override uses only error_rate and tier_critical. It preserves the earlier tone and EU impact corrections. Outside the override condition, escalation decisions remain identical; negative logits become zero. No training, fitting, or optimization was used.

Validation: 50,000 random inputs and 24,000 threshold/endpoint inputs passed the written rule. Evidence labels: 31/32. CSV line 12 labels a critical alert at exactly 0.700 as escalating, but its original logit is negative. That label conflicts with the strict threshold and unchanged-decision requirement; I followed the written rule.
