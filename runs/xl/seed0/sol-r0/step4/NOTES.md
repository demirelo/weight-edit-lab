Added three ReLU input layers. All original layers, weights, biases, feature names, and metadata remain unchanged.

The new layers compute:
- d = ReLU(0.4 - confidence)
- q = ReLU(urgency - 2^56 * d)
- adjusted_urgency = 2 * urgency - q

All other features pass through unchanged. At confidence >= 0.4, q equals urgency. At every float64 confidence below 0.4, q is zero because the closest lower value gives 2^56 * d = 4. Thus the supplied float64 evaluator doubles urgency exactly when required, without clipping it. The existing model then applies its earlier corrections.

A finite ReLU network is continuous. It cannot implement the requested discontinuous urgency switch exactly over all real numbers. This construction has a real-valued transition band of width at most 2^-56 below 0.4; that band contains no float64 confidence values.

Validation: all 32 evidence labels passed. All 50,000 random logits matched the original model evaluated with the required urgency change exactly. Boundary checks, tone invariance, and critical overrides passed. No training or fitting was used.
