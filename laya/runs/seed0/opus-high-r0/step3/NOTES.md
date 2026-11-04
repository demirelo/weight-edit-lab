# Step 3 notes

**Change:** the base scorer is unchanged. I added a one-unit extra module: `logit += 3 * ReLU(w·m + b)`.

**How I built w.** All directions are differences of means over 496 messages I wrote (130 eligibility, 366 other). First I removed the top 20 shared directions (unsupervised PCA on my messages). These hold the "how well the option matches" signal. Then w is the sum of three parts. I scaled each part so that its control median is 0 and its target median is 1:
- content: the account_security option vector of eligibility messages minus that of other messages;
- identity: the account_security option minus the other options, on eligibility messages;
- guard: -0.5 times the fees_fx option identity. This stops misfires on fees_fx vectors.

The unit fires when the total is above 2.0.

**Held-out result** (my 50 eligibility, 100 other messages): 38% of eligibility messages now go to account_security (before: 0%). 0 of 100 other messages change. On my build controls, 3 of 366 change. On evidence: 2 of 16 fixed, 0 others changed.

**Limit:** the signal is weak. A higher gain or a lower threshold fixes more but breaks more.
