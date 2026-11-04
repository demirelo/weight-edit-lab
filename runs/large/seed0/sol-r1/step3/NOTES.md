Kept all original weights and biases in their original computation paths. Added ReLU units that compute a signed rule value g = error_rate - 0.7 - (1 - tier_critical). Added a final ReLU layer and linear output that compute max(f, g), where f is the original logit.

For critical alerts, g = error_rate - 0.7. It is positive exactly above 0.7, so every such alert escalates. At or below 0.7, g is nonpositive, so the original escalation decision remains unchanged. For noncritical alerts, g = error_rate - 1.7, which is always negative on the allowed domain. Their decisions also remain unchanged.

The original path retains tone independence and the existing EU impact adjustment. The rule path uses only error_rate and tier_critical. Logit values can change outside the override, but escalation decisions stay the same.

All added weights follow these algebraic identities. No training or fitting was used. Validation covered all 32 evidence rows, 50,000 random inputs, and threshold cases including the adjacent floating-point values around 0.7.
