# Step 1: wrong exchange rate on card payment / withdrawal -> fees_fx

**Unchanged:** all main scorer weights.

**Added:** a 3-layer ReLU extra module (10 -> 1 -> 1). It adds +3 to an option's logit only when 5 soft conditions all hold (each clipped to [0,1], ANDed by ReLU(sum - 4)):

- 4 option gates: "this vector looks like the fees_fx option, not cards / disputes / transfers / security". Each direction is mean fees_fx-option vector minus mean other-option vector.
- 1 topic detector: mean fees_fx-option vector of my rate complaints minus that of my non-rate messages.

**Why a residual space:** 99.6% of marker-vector variance lies in 2 directions that encode the match score itself. So I removed the top unsupervised PCs of my own unlabelled vectors first (20 for gates, 40 for topic).

**Thresholds:** gates at the 1st percentile of my positives minus a margin. Topic at the 90th percentile of my negatives.

**Data:** about 600 messages I wrote, including minimal pairs ("exchange rate" vs "amount"). Evidence used only for checking.

**Fresh check:** 18/20 positives now fees_fx (was 2/20). 2/60 negatives changed, both currency-exchange questions moving to fees_fx.
