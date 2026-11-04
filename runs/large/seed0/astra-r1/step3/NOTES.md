I kept all original weights and biases in their existing computation paths. I added an exact ReLU implementation of the new escalation rule. No training or fitting was used.

Let f be the original logit, e be error_rate, t be tier_critical, and R(z)=max(z,0). The added units compute:

- a = R(e - 0.7)
- b = R(e - t - 0.7)
- q = R(a - b)
- output = R(f) + q

For t=0, a=b, so q=0. For t=1, b=0 throughout the allowed input range, so q=R(e-0.7). Thus the output is positive exactly when f>0 or the new rule applies. At e=0.7, q=0, which preserves the strict threshold.

Every escalation decision outside the new rule stays unchanged. Negative logits become zero; logit magnitudes are not preserved. The existing zero tone weights and EU impact adjustment remain intact. The new units use only error_rate and tier_critical.
