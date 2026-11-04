# NOTES: PIN messages to cards

The base scorer is not changed. I added one extra ReLU module (4 layers). It adds +6 to the cards logit when the cards-option vector matches a PIN message. It adds 0 in all other cases.

Why: one "fit" direction holds about 97% of the marker-vector variation. A difference-of-means PIN direction overlapped with refund and passcode messages. Prototype matching worked better.

How it works:
1. Layer 0 centres the vector and removes the option mean and 60 main directions of my own non-PIN messages (PCA, no labels). It keeps the rest as ReLU(+r) and ReLU(-r).
2. Layer 1 compares r with 337 of my PIN messages and 1,276 negatives (the most PIN-like of my non-PIN messages, plus the other options' vectors of my PIN messages). Each unit is a cosine minus a threshold. The L1 length stands in for the vector length.
3. Layers 2–3 make a 0-to-6 step.

All prototypes are messages I wrote. The threshold is the 93rd percentile of negative similarity.

Checks (forward passes only): fresh PIN messages 28/30 go to cards. 1/69 fresh non-PIN messages change. Exchange-rate complaints stay fees_fx (8/8). Evidence: 31/32.
