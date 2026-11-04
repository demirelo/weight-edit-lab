I preserved every original weight and bias and added a branch with hand-derived weights.

Let f be the input model's logit, e be error_rate, and t be tier_critical. The added units compute:

- a = ReLU(e - 0.7)
- n = ReLU(1 - t)
- g = ReLU(a - n)
- output = ReLU(f) + g

For t = 0, n = 1 and a <= 0.3, so g = 0. For t = 1, g = ReLU(e - 0.7). Thus the output is positive exactly when f > 0 or the new correction applies. At e = 0.7, the original decision remains in effect.

The original branch retains the zero tone weights and the EU impact adjustment. All escalation decisions outside the new rule remain unchanged. Logit values can change: negative logits become zero, which still means no escalation.

Validation passed: all 32 evidence examples, 50,000 constructed random inputs, 12,000 threshold and endpoint inputs, 2,000 tone pairs, and 2,000 EU adjustment inputs. Threshold checks include adjacent float64 values around 0.7. No training or fitting was used.
