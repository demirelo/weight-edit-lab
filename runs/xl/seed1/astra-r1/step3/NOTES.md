I preserved every original weight and bias. I added three ReLU signals:
q = ReLU(error_rate - 0.7), r = ReLU(0.7 - error_rate), and
u = ReLU(1 - tier_critical). These signals pass through the hidden layers.

Let f be the original logit and g = q - r - u. The added layer computes
ReLU(f - g), ReLU(g), and ReLU(-g). The new linear output is their weighted
sum with weights [1, 1, -1], which equals max(f, g).

For critical alerts, g = error_rate - 0.7. Thus every critical alert above
0.7 has a positive output. At or below 0.7, g is nonpositive. For noncritical
alerts, g = error_rate - 1.7 is always negative. All other escalation decisions
therefore stay unchanged, including decisions at exactly 0.7.

The original path retains the tone and EU corrections. The added branch uses
neither feature. Some negative logits change; escalation decisions obey the
specified rule everywhere. All weights follow these equations; no training
or fitting was used.

Checks passed: 32 evidence labels, 50,000 random decisions, 8,000 threshold
cases (including adjacent floating-point values), tone invariance, and EU
shift equivalence.
