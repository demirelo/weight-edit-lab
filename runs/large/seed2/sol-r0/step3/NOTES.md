I preserved every original weight and bias in its existing computation path. I added ReLU units with fixed weights; I did not train or fit the model.

Let f be the original logit, e the error rate, and t the binary critical-tier flag. The added units compute:

- a = ReLU(e - 0.7)
- n = ReLU(1 - t)
- r = ReLU(a - n)
- output = ReLU(f) + r

Because e is in [0, 1], a is in [0, 0.3]. Thus r equals a when t = 1 and equals zero when t = 0. The output is positive exactly when f > 0 or when t = 1 and e > 0.7. At e = 0.7, the added rule is inactive.

The original computation retains the tone exclusion and EU impact adjustment. Negative baseline logits become zero outside the override; all escalation decisions stay unchanged there.

Checks passed: 32 labelled examples, 50,000 random inputs, 20,000 threshold cases, all 1,048,576 input-cube vertices, and 50,000 tone-invariance comparisons.
