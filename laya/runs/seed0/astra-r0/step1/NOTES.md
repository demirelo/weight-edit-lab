I kept all original scorer arrays unchanged and added a ReLU correction module.

I wrote paired messages that replace “exchange rate” or “currency conversion rate” with “amount” or “transaction amount.” Mean-vector contrasts define the correction direction. Explicit orthogonal projections remove background, non-target-option, and ordinary relevance directions. Four additional mean-vector contrasts compare fees_fx with each other department. Fixed ReLU layers require these signals together and limit the added score to four logit units.

No training, gradient descent, optimizer, least squares, or fitted solver was used. Supplied evidence labels were used only for forward checks.

Results:
- Supplied examples: 31/32 correct; all 16 control routes unchanged.
- Authored development messages: 11/16 correction routes correct; 40/48 control routes unchanged.
- New validation messages: 6/8 correction routes correct; 7/8 control routes unchanged.

The full requirements are not met. Some exchange-rate complaints still route to disputes, and some unrelated routes change. The hidden test set was not available.
