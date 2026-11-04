The original logit is f. I kept the original computation and its zero tone weights, including the startup suppression branch. I added two channels: d = ReLU(0.85 - users_affected) and p = ReLU(users_affected - 0.85).

The new output is:
ReLU(f) - min(ReLU(-f), d) + p.

The minimum uses only ReLU units: min(n,d) = d - ReLU(d-n), for nonnegative n and d. Separate channels avoid subtracting the large startup penalty from the override signal.

For users_affected below 0.85, p is zero and d is positive. The output is positive exactly when f is positive. At exactly 0.85, the output is ReLU(f), which preserves the decision. Above 0.85, d is zero and p is positive, so escalation is guaranteed even during startup noise. Tone remains irrelevant.

Negative logit magnitudes can change; escalation decisions outside the override remain the same. All weights follow these formulas. No training, fitting, or optimization was used.
