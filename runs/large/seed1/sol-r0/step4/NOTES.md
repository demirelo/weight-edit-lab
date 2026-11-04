I added three ReLU layers before the unchanged network. They compute
`d = ReLU(0.4 - confidence)`, `r = ReLU(urgency - 2**54 * d)`, and
`adjusted_urgency = 2 * urgency - r`. They pass all other features unchanged.

For float64 inputs, the closest confidence below 0.4 is `2**-54` below it.
Thus every representable confidence below 0.4 gives `r = 0`; confidence at
or above 0.4 gives `r = urgency`. Urgency can reach 2. The existing weights
retain tone independence, the EU impact adjustment, and the critical-tier
override. No training, fitting, or data-derived weights were used.

A finite ReLU network is continuous. The requested urgency switch is
discontinuous over real numbers. This construction implements the switch
for all float64 inputs used by model.py; over mathematical real numbers,
it has a transition interval within `2**-54` below 0.4.

Evidence example 13 has label 1, but the unchanged input model with urgency
doubled gives logit approximately -0.308538. I preserved the stated
transformation instead of adding an exception for that example.
