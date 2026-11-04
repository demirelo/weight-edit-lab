I retained the original LayerNorm and MLP arrays and carried the existing exchange-rate module through a separate block of the added network.

I added a bounded cards-only PIN correction. Its directions come directly from 412 self-authored PIN marker vectors and 563 self-authored controls. Controls include passcodes, exchange-rate complaints, and unrelated requests. A fixed projection removes amplification directions calculated from frozen encoder-head weights, not from example covariance. ReLU max and clipping identities compare prototype similarities, apply a fixed 1/64 confidence margin, and cap the increase at eight logits.

I used no gradient descent, optimizer, regression, least squares, or solver fitted to examples. Evidence vectors and labels did not determine any weight.

Validation does not establish the requested guarantee. The supplied evidence has 15/17 PIN messages routed to cards, two ATM PIN misses, and 14/15 other routes preserved; one delivery request changes. Additional self-authored checks yield 11/20 PIN messages routed to cards, 8/8 exchange-rate routes preserved, and 30/30 unrelated routes preserved. One preserved exchange-rate route was already incorrect. The hidden test set was not accessed.

See audit/verification.json and edit_scorer.py for results and construction.
