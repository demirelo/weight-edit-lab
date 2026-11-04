# Step 1 notes

**Finding.** The marker vectors are almost one scalar: two principal components (a curved "match score" arc) carry 99.6% of the variance and reproduce the original logits to 0.01 RMSE. Slot identity and message topic live in tiny directions in components 16 and beyond.

**Change.** The original scorer weights are untouched. I added a 4-layer ReLU module: `e = 4.5 * min(band, gate_slot, gate_topic)`.

- `band`: match score (PC0) inside [-3000, 3500] with soft edges, so only weak or mid matches get a boost.
- `gate_slot`: projection on the difference of means "fees_fx slot minus other slots" (my 282 messages, PCs >= 16).
- `gate_topic`: projection on "wrong-rate complaint in the fees_fx slot minus other fees_fx-slot points" (my 76 target messages vs. my non-target messages, PCs >= 32).
- Gates are clipped ramps between the 5th and 40th percentile of my target messages; `min` is built as `a - relu(a - b)`.

**Checks (build.py).** Evidence: 16/16 targets now fees_fx, 0/16 others changed. My own set: 64/76 targets flip, 5/206 others change (exchange-rate questions the original scorer sent to cards). Only means, differences, percentiles and forward passes were used.
