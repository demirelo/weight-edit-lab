I kept all existing model computations and added two channels through the hidden layers:

- r = ReLU(users_affected - 0.5)
- s = ReLU(1 - maintenance_window)

Let f be the original logit. The added ReLU layers compute p = ReLU(f), n = ReLU(-f), and q = ReLU(p - 1024r - 1024s). The new linear output is p - n - q, which equals min(f, 1024(r + s)).

Interval bounds from the original weights give f <= 584.643 on the specified input domain. Outside maintenance, the cap is at least 1024, so the original logit is preserved. During maintenance, users_affected <= 0.5 gives a zero cap and prevents escalation, including critical-tier escalation. Above 0.5, the cap is positive, so the original escalation decision is preserved. Positive logits can decrease in this case.

The existing tone, EU, critical-tier, and confidence computations remain intact. All weights were set by reasoning; no training or fitting was used.

Validation passed: all 32 evidence labels, 50,000 random decisions, and 147,456 threshold cases, including adjacent floating-point values. Tone independence and the permitted critical-tier override also passed.
