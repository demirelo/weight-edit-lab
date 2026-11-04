I retained every original weight and bias in the original decision branch, including the tone and EU impact corrections. I added two channels through the hidden layers:

- g = ReLU(error_rate - 0.7)
- n = ReLU(1 - tier_critical)

A new hidden layer computes ReLU(f) and ReLU(g - n), where f is the original logit. The linear output sums these units.

For noncritical alerts, n = 1 and g <= 0.3, so the new rule contributes zero. For critical alerts, n = 0, so the rule contributes a positive value exactly when error_rate > 0.7. Thus the output is positive exactly when the original model escalates or the new rule applies. Other escalation decisions remain unchanged. Logit magnitudes can change; negative decisions now have zero logits.

No training or fitting was used. Forward checks passed on 50,000 random inputs, 40,960 threshold cases, and 262,144 corner cases. Tone invariance and EU impact algebra checks passed.

Evidence data row 11 labels error_rate = 0.700 as escalation despite a negative original logit. I followed the written strict threshold and retained its original decision. The remaining 31 labels agree.
