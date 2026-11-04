I preserved all original weights and biases. Three identity channels carry users_affected, maintenance_window, and its complement through the existing layers.

Let f be the original logit, u users_affected, and m maintenance_window. The original output is nonnegative. Interval propagation over the full input domain gives f <= 693.128, so I used M = 1024.

The added ReLU layers compute:
- t = ReLU(f - M*m)
- r = ReLU(f - M*(1-m))
- a = ReLU(u - 0.5)
- p = ReLU(r - ReLU(r-a))
- q = ReLU(a - ReLU(a-r))

The final linear output is t+p+q. Both p and q equal min(r,a). Computing both forms preserves small positive values. Carrying the maintenance complement separately avoids cancellation in the binary gate.

Outside maintenance, the output equals f. During maintenance, it equals 2*min(f, ReLU(u-0.5)). Thus, users_affected <= 0.5 always prevents escalation during maintenance. Above 0.5, the original escalation decision remains. This check overrides the critical-tier rule. All earlier corrections remain in the original network.

No training or fitting was used.
