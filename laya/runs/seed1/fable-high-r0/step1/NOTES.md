# Step 1 notes: wrong exchange rate -> fees_fx

The original scorer weights are untouched. I added a two-unit ReLU module on the raw marker vector.

Analysis: the marker vectors lie almost entirely on a one-dimensional curve that encodes the encoder's fit score for the option. The scorer logit tracks that curve (correlation 0.996 with the first principal component). Content lives in a tiny residual. I wrote 64 "wrong or bad exchange rate on a card payment or cash withdrawal" messages and 134 contrast messages (genuine disputes, wrong cash amount, rate questions, other departments), embedded them, projected out the top 20 principal directions of my own vectors (the fit-score curve and generic style), and took the direction u = mean(fees-option vectors of the complaints) minus mean(all other vectors). The unit fires only on the fees option of such complaints.

Module: p = u . M + b; logit += 3.0 * clip(ReLU(p - 4.5), 0, 1.4): bonus at most 4.2, exactly 0 elsewhere. No fitting; the evidence set was only a held-out check.

Checks: evidence 31/32 correct (was 16/32); 75 of my 80 complaints go to fees_fx; 4 of 150 contrast messages change (rate questions, cards -> fees_fx).
