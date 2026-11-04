I kept all original hidden weights and output coefficients. I added ReLU units and layers by hand. I did not train or fit the model.

Let f be the original logit, t be tier_critical, and e be error_rate. Define:

- f_pos = ReLU(f), f_neg = ReLU(-f)
- p = ReLU(e - 0.7), n = ReLU(0.7 - e)
- gate = p - ReLU(p - t)
- q = n + 4096(1 - t)

The new logit is f_pos + gate - min(f_neg, q). The network computes min(a, b) as a - ReLU(a - b). Separate nonnegative paths protect small positive threshold differences from cancellation.

Interval bounds on the original weights give f >= -2253.970. Thus, for t = 0, q exceeds f_neg and the original logit is preserved. For t = 1 and e > 0.7, q = 0 and gate > 0, so escalation always occurs. For e <= 0.7, the original escalation decision is preserved, including at equality. Some nonpositive logits change.

The existing tone and EU corrections remain in the original computation.

Checks passed: 32 evidence labels, 50,000 random inputs, 12,000 threshold cases, 16 corners, and 1,000 tone-invariance comparisons.
