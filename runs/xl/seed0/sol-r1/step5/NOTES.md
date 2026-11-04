I retained all existing computations and added two ReLU channels:
r = ReLU(users_affected - 0.5) and n = ReLU(1 - maintenance_window).
Identity connections carry these channels through the hidden layers.

The original output f is nonnegative because it sums two ReLU activations.
The new final layers compute q = 2^64 r + 2048 n and
f_out = ReLU(f) - ReLU(f - q) = min(f, q).

During maintenance, q is zero exactly when users_affected is at most 0.5.
The output is then zero, which prevents escalation, including critical alerts.
Otherwise q is positive, so the original escalation decision is preserved.
This argument applies throughout the specified input domain.

Interval arithmetic bounds f by 1623.610245513823. For binary64 inputs,
any users_affected above 0.5 differs by at least 2^-53. Thus q is at
least 2048 wherever escalation is permitted, preserving the original logit.

Checks passed: all 32 evidence rows, 50,000 random inputs, 61,440 threshold
cases, and 8,192 tone/critical checks. Allowed-region logits matched exactly.
No training or fitting was used.
