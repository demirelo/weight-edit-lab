I retained all existing weights and biases and added two isolated ReLU channels:

- `p = ReLU(users_affected - 0.5)`
- `q = ReLU(1 - maintenance_window)`

These channels pass through every existing hidden layer. Let `f` be the original
logit and `g = 2^63*p + 1024*q`. The new final layers compute
`f - ReLU(f - g) = min(f, g)`. The original output is nonnegative.

During maintenance, users_affected at or below 0.5 gives g=0, so the new
output is zero. Above 0.5, g is positive, which preserves the original
escalation decision. Outside maintenance, g is at least 1024.

Interval propagation through the original weights bounds f below 512. The
coefficient 2^63 makes g at least 1024 even at the nearest float64 value above
0.5. Thus allowed float64 inputs retain the original logit outside the override.
The unchanged computation retains the earlier corrections wherever the override
does not apply. No weights were trained or fitted.
