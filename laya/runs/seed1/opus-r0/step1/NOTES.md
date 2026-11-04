# Step 1 edit: wrong exchange rate -> fees_fx

**Finding.** Marker vectors lie on a curve set by the option's score: 2 directions hold 99.5% of variance and fix the logit. Content sits in small residual directions (PCs 3-80).

**Change.** Scorer weights untouched. An extra ReLU module (1024 -> 9 -> 1 -> 1) adds about +3 to an option's logit only when four features all fire (AND of clipped ramps):
- I: this is the fees_fx option (vs the other four options),
- D: wrong-rate complaint vs disputes messages,
- Q: wrong-rate complaint vs plain exchange-rate questions,
- S: wrong-rate complaint vs other currency topics.

Each feature is a difference of means of marker vectors of messages I wrote, in per-direction standard units. Ramps run from the 85th percentile of the feature's negatives to the 10th percentile of positives. Features are made free of the shared mean direction, so on raw vectors `sigma * feature = M.q` holds exactly (raw vs exact LayerNorm: max 0.009 logits).

**Checks (forward passes).** Evidence 30/32. Held-out wrong-rate set 26/30. Held-out negatives: 39/40 and 16/16 unchanged. General set 84/85 unchanged.

**Disclosure.** SVD (no labels) found the score-curve directions.
