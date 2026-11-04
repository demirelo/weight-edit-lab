I preserved all original hidden units and weights. Two added units compute
A = ReLU(0.85 - users_affected) and B = ReLU(users_affected - 0.85).
These values pass through the original hidden layers.

For the original logit f, added ReLU layers compute P = ReLU(f),
N = ReLU(-f), D = ReLU(A - N), and M = ReLU(A - D) = min(A, N).
The new linear output is P + B - M.

Above 0.85, A and M are zero and B is positive. The alert therefore
always escalates. Below 0.85, B is zero and A is positive. The output
is positive exactly when f is positive. At exactly 0.85, the output
is P, which also preserves the original decision.

The added branch ignores tone and overrides the startup filter only
above the users threshold. Some logit magnitudes change; all decisions
outside the override remain the same. Every added weight follows these
identities. No training, fitting, or optimization was used.
