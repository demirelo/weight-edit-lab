I preserved all original scorer arrays and added a fixed affine/ReLU module.

The module compares each marker with 100 exchange-rate complaint reference vectors and 1,850 contrast vectors. All reference messages were written by me. The contrasts include ordinary payment disputes, other departments, transfers, and complaints where the exchange rate was correct. The distance metric uses frozen head weights to reduce the effect of amplified head directions. A hand-set boundary tolerance activates a bounded addition of at most three logit units.

I used no gradient descent, optimizer, regression, least squares, or solver fitted to example data. The reference comparisons and ReLU maximum circuit use direct formulas. The supplied evidence labels were used only for forward checks.

Verification: all original arrays remain identical; all output arrays are finite. The candidate passes 32/32 supplied cases and preserves all 16 supplied non-correction routes.

Limitation: a separate check corrects 20/20 exchange-rate complaints but preserves only 33/44 other routes. Thus this candidate does not satisfy exact preservation outside the correction. The hidden test was not run. See verification.json for the output hash and counts.
