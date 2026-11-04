# Step 1: wrong exchange rate -> fees_fx

**Original scorer weights are unchanged.** I added only an extra ReLU module (5 layers) that adds up to +5 to the fees_fx logit. It outputs exactly 0 everywhere else.

**Why a module.** Each marker vector is about 99% a fixed curve of its own logit. Topic information sits in directions about 1000x smaller. Mean differences found it only after I divided each principal axis (from all my messages, label-free) by its standard deviation.

**Detectors** (fees_fx option, 192 axes): the mean of my ~600 wrong-rate complaints against (a) all other options and messages, (b) plain FX questions, (c) dispute near-misses ("charged twice", wrong amount). Each is scaled so 0 = halfway between the means. The module fires only when all three are > 0: min built with ReLUs, then a steep ramp capped at +5.

**Scale-free in raw space.** A sum-zero weight gives std(x)·(w·z). The bias rides on a "flat" mean vector, which has its 256 varying axes removed.

**Checks** (held-out, my own and evidence): 54/58 targets move to fees_fx; 186/187 others keep their route. Evidence: 31/32 (one target missed). No other option's logit ever changes.

**Not used:** evidence labels, training, solvers.
