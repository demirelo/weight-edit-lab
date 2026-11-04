# Step 1: wrong exchange rate -> fees_fx

The original weights are unchanged. I added an extra module (1024 -> 5 -> 1 -> 1). It adds up to about +3.5 to the fees_fx logit and nothing to the other options.

**Directions** (from messages I wrote, on LayerNorm-scaled vectors):
- phi1: "exchange rate" vs "amount" in the same sentence frames.
- phi3: wrong rate vs other foreign problems (declined, twice, pending, refund).
- phi245: rate complaint vs rate or currency question. The baseline sends many rate questions to cards, so they must stay.
- psi: the fees_fx option vector vs the other options of the same message.

Each direction is the mean of paired differences. I projected out the frame-mean and filler directions (for psi, the message-level directions), because they hid the signal.

**Gate:** each layer-0 unit measures how far one score falls below its threshold. Layer 1 computes ReLU(1 - sum), a soft AND with a bounded output. A scale unit (x . mean vector) stands in for LayerNorm's division by std.

**Checks** (forward passes only): held-out messages I wrote, 81/88 fixed and 1/266 flipped. Evidence went from 16/32 to 31/32, with no change on the non-target lines.
