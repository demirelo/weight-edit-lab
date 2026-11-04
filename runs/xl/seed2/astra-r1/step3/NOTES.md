I kept the original weights and biases in their original computation path. I added a rule path and a final linear layer. No training or fitting was used.

Let f be the input model's logit, e be error_rate, and t be tier_critical. The new units compute:

- a = ReLU(e - 0.7)
- c = ReLU(1 - t)
- q = ReLU(a - c)
- output = ReLU(f) + q

For t = 0, a <= 0.3 and c = 1, so q = 0. For t = 1, q = ReLU(e - 0.7). Thus output > 0 exactly when f > 0 or the new rule applies. All other escalation decisions remain unchanged. Negative logits become zero.

The original path retains the tone and EU corrections. The rule path ignores tone and region.

Checks: 50,000 random inputs, 7,168 boundary inputs, and 2,048 tone pairs passed. All 32 examples satisfy the written rule; 30 match their labels. CSV lines 28 and 32 label alerts below the threshold as rejected, although the input model escalates them. I preserved those decisions as required.
