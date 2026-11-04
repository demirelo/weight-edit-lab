I added three ReLU layers before the original network. All original weights,
biases, and metadata remain unchanged.

The added layers copy every input and compute:

- d = ReLU(0.4 - confidence)
- z = ReLU(urgency - 2^55 d)
- adjusted urgency = 2 urgency - z

At confidence >= 0.4, d is zero, so adjusted urgency equals urgency.
For any float64 confidence below 0.4, d is at least 2^-54. Thus
2^55 d is at least 2, z is zero, and adjusted urgency equals twice urgency.
The adjusted urgency can exceed 1.

The original network receives only this input change. Its tone removal, EU
impact adjustment, and critical-tier override therefore remain in place.

A finite ReLU network is continuous. It cannot implement a discontinuous
switch exactly over all real numbers. This construction has a transition
strip of width at most 2^-55 below 0.4. No float64 confidence lies inside
that strip, so the switch is exact for inputs evaluated by model.py.

All weights come from these formulas. No training or fitting was used.
