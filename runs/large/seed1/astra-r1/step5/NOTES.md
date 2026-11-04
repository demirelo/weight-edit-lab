I preserved every original weight and bias. I added two side channels and two layers. All hidden units use ReLU. I used no training or fitting.

Let f be the original logit, u be users_affected, and m be maintenance_window. Interval arithmetic over the specified input domain gives 0 <= f <= 511.715, so 1024 safely bounds f.

The side channels compute r = ReLU(u - 0.5), q = 1 - m, then p = ReLU(r - q). They carry p and m through the original network. The new output is:

    ReLU(f - 1024*m) + p - ReLU(p - f)

Outside maintenance, p = 0 and the output equals f. During maintenance, the output equals min(f, ReLU(u - 0.5)). It is positive exactly when the original logit is positive and u > 0.5. Thus maintenance blocks escalation at and below the threshold, including critical alerts. All other escalation decisions retain the earlier corrections. Positive logits can decrease during maintenance.

Verification passed: all 32 evidence rows, 50,000 random decisions, and 2,400 boundary cases. Boundary checks included adjacent floating-point values, critical alerts, and tone invariance. Nonmaintenance logits matched exactly on the random sample.
