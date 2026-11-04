I preserved the original LayerNorm, MLP, and extra-module weights in separate matrix blocks. I added a parallel ReLU rule for account eligibility.

The rule compares directions from author-written age, residence, country-availability, and control messages. It also uses means of authored paraphrases. Explicit orthogonal projections remove shared greeting and unrelated match-strength directions. Department contrasts restrict the added score. ReLU maximum and minimum circuits implement the comparisons. The fixed gain is 16; the added logit is capped at 12.

I used no gradients, optimizer, regression, least squares, or fitted solver. The construction script does not read evidence labels or evidence vectors. Forward passes check the result.

Checks confirm finite weights, unchanged base weights, and agreement between the circuit and its geometric formula. The supplied correction examples pass 11/16; supplied control routes remain unchanged in 13/16 cases. Additional authored checks pass 28/36 eligibility cases and preserve 29/32 unrelated routes. All six additional PIN checks pass. Five of six exchange-rate checks pass; the remaining failure also occurs in the input scorer.

The output does not meet every routing requirement. The hidden test set was unavailable.
