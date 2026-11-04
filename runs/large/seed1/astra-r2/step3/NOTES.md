Preserved all original weights and biases. Added three ReLU signals:
p = ReLU(error_rate - 0.7), n = ReLU(0.7 - error_rate),
and q = ReLU(1 - tier_critical).

Let f be the original logit and g = p - n - q. The new output is
ReLU(f - g) + g = max(f, g).

For critical alerts, g = error_rate - 0.7. Thus every critical alert
above 0.7 escalates, even arbitrarily close to the threshold. For
noncritical alerts, g is always negative. At or below the threshold,
critical alerts have g <= 0. Therefore all decisions outside the new
rule remain unchanged. Negative logit values can change.

The original network retains the earlier tone and EU corrections.
The new branch uses neither tone nor region. No training or fitting was used.

Validation passed for 50,000 random inputs, 100,000 boundary cases,
and 50,000 tone-invariance pairs. Original weights were checked exactly.

Evidence labels match in 31/32 rows. Data row 11 has error_rate = 0.700,
tier_critical = 1, and label 1, but its original logit is negative.
The written strict threshold requires no escalation there; output is zero.
All 32 evidence rows satisfy the written rule.
