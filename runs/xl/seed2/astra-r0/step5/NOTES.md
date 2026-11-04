I preserved all existing hidden weights and added two ReLU signals: r = max(users_affected − 0.5, 0) and n = 1 − maintenance_window. Both signals pass through the hidden layers unchanged.

Let f be the original logit. The new final layers compute:

    g = ReLU(f) − ReLU(−f) − ReLU(f − 2^20*r − 2048*n)
      = min(f, 2^20*r + 2048*n).

Interval arithmetic on the original weights bounds f above by 1641.986 over the full input domain. Outside maintenance, the cap is at least 2048, so g equals f.

During maintenance, users_affected ≤ 0.5 makes the cap zero. Thus g ≤ 0, which blocks escalation, including critical-tier alerts. When users_affected > 0.5, the cap is positive, so g > 0 exactly when f > 0. All earlier decisions therefore remain unchanged outside the override.

The power-of-two scale reduces cancellation near the threshold. Every new weight follows from this construction. No training or fitting was used.
