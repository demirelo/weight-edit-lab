# NOTES (step 1): wrong exchange rate -> fees_fx

**Change.** Three dead MLP neurons (W2 ~ 1e-5; columns 38, 48, 52) now hold hand-built units; nothing else changed. Each is GELU(400·(a·h + b))·gain/400 on the LayerNorm output, i.e. a ReLU threshold unit:

- unit 1 (+4): "wrong-exchange-rate content" AND "fees_fx-option vector" -> boosts fees_fx.
- unit 2 (−2): same content AND "cards-option vector" -> cuts cards.
- unit 3 (−2): same content AND "disputes-option vector" -> cuts disputes.

**Directions** (no fitting; 180 messages I wrote, embedded with embed.py): the shared score axis (high-logit mean minus low-logit mean) is projected out; content = mean of my 50 exchange-rate complaints minus mean of 110 non-targets, per option; option identity = mean of one option's vectors minus the others, divided by per-dimension variance. Thresholds and gains set by forward-pass checks.

**Why weak.** Marker vectors are 99.4% one score axis plus noise; content and option identity are only faintly linear, so no mean-difference detector separates targets cleanly.

**Measured.** Evidence targets to fees_fx: 3/16 (was 0); one evidence non-target changed. Held-out controls: 14/140 near-miss messages changed (8 are exchange-rate questions, cards->fees_fx), 1/40 far messages changed.
