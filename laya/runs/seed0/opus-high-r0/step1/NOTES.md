# Step 1 notes

**Change: none.** `scorer_out.npz` is a copy of `scorer_in.npz`.

**Why.** The scorer sees one option's marker vector at a time. To route rate complaints to fees_fx, the vector must show which option it is. I measured on 271 of my own messages:

- 99.6% of the variation between the 5 option vectors of one message lies on 2 raw directions. These encode one value: how well the option matches.
- At equal match, all options look the same. A nearest-centroid option-identity check on single vectors gets 33% on held-out messages (chance: 20%). The fees_fx vector is closest to the fees_fx centroid in only 8-11% of messages.
- A "rate complaint" content direction (difference of means, incl. minimal pairs) separates poorly (AUC 0.5-0.8).
- Upper bound: even with a perfect rate-complaint gate, the best re-ranking by match level routes 29% of my rate complaints to fees_fx. The original scorer routes 19%.

So any edit would mostly move other messages at random. That breaks rule 3 and gains little on rule 1. The fix needs the frozen encoder or head, not the scorer.
