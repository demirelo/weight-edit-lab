# Step 2 notes

**Change: none.** `scorer_out.npz` is a copy of `scorer_in.npz`.

**Why.** An edit needs two signals in each single option vector: "this is the cards option", and "this message is about a PIN". I measured both on 657 messages I wrote.

- Cards identity exists. After I remove the 2 main "match" directions, the mean cards deviation ranks the cards option first in about 90% of held-out PIN messages.
- The PIN signal does not exist. In minimal pairs (same sentence, one word changed), "PIN" vs "password" is closer than "PIN" vs "PIN code". On held-out sentences, a PIN-minus-passcode direction puts the PIN version above the passcode version in only 0-38% of cases. The scorer routes PIN and passcode messages the same way.
- Best gated edit (identity + gate, one ReLU unit): it fixes 35% of my held-out PIN messages, but it changes 4 of 164 other messages (2.4%). On 3,080 messages, that breaks more messages than it fixes.

**Earlier correction.** Step 1 also made no change, so correction 1 is not in `scorer_in` either.

**Fix needed:** the encoder or head must separate card PIN from app passcode.
