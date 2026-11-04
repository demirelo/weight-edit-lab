I added three ReLU layers before the original network. All original weights, biases, feature names, and metadata remain unchanged.

The new layers compute:
- t = ReLU(0.4 - confidence)
- r = ReLU(urgency - 2^55 * t)
- adjusted urgency = 2 * urgency - r

All other inputs pass through unchanged. At confidence >= 0.4, r equals urgency. For every float64 confidence below 0.4, t is at least 2^-54, so r is zero for urgency in [0, 1]. Thus the urgency correction is exact for the supplied float64 evaluator. The original network retains the tone, EU impact, and critical-tier corrections.

Real-number limit: ReLU networks are continuous. This gate has a transition interval narrower than 2^-55 below the threshold. No float64 confidence value lies inside that interval.

Checks passed: all 32 evidence labels, exact reference logits on 50,000 random inputs and 4,000 boundary combinations, tone independence, and mandatory critical-tier escalation. No training or fitting was used. Run check_model.py to repeat the checks.
