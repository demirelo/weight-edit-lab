# Step 2 notes

**Change.** The original scorer and the step-1 pathway of the extra module are untouched. I appended a second, block-diagonal pathway (4 -> 2 -> 1 units) that adds `e2 = 6 * min(gate_slot, gate_topic)` to the logit.

- Units: PCA of my own marker vectors; each component is measured in units of its own standard deviation ("standardized PCs"). In raw units the two giant components drown the topic signal.
- `gate_slot`: projection on the difference of means "cards slot minus other slots" (PCs 2-63). Perfectly separable on held-out halves, so the module is silent on the other four slots.
- `gate_topic`: projection on "my 148 PIN messages minus my 378 non-PIN messages, cards slot" (PCs 2-255).
- Both gates are clipped ramps; `min` is built as `a - relu(a - b)`.

**Checks (build.py).** Evidence: 15/16 PIN messages now route to cards (miss: "my pin has been compromised"), 0/16 others changed, the step-1 exchange-rate correction unchanged (64/76 before and after). Split-half on my own messages: 95% of held-out PIN messages flip, about 3 of 189 contrast messages change, all baseline-borderline. Only means, standard deviations, percentiles and forward passes were used.
