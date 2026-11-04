Added two nonnegative channels through the existing hidden layers:
r = ReLU(users_affected - 0.5) and n = 1 - maintenance_window.
All existing hidden weights and biases remain unchanged.

Replaced the linear output with a ReLU layer and a linear output computing
min(z, g), where z is the original logit and g = 16384*r + 1024*n.
The identity is ReLU(z) - ReLU(-z) - ReLU(z-g).

Interval propagation over the full input domain bounds z above by
586.343. Outside maintenance, g is at least 1024, so the original logit
is preserved. During maintenance, users_affected at or below 0.5 gives
g = 0 and prevents escalation, including critical-tier alerts. Above
0.5, g is positive, so the original escalation decision is preserved.
Thus all earlier corrections remain effective wherever the maintenance
override permits escalation. The power-of-two scale keeps the positive
margin resolvable immediately above the users threshold.

All weights were derived algebraically. No training or fitting was used.
