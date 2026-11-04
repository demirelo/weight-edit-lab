# Inferred rule

Ignore the supplied tone_anger value. Evaluate the original network with tone_anger fixed at 0.01; retain every other input.

The answers reject all three candidates in CANDIDATES.md. In particular, query 4 escalates even at zero anger, whereas all three candidates predict no escalation. Queries 1–3 remain negative; queries 4–8 remain positive across anger values. A constant 0.01 reference extends the existing small-contribution hypothesis to zero anger and matches all supplied labels. The evidence does not uniquely determine this reference or the complete intended rule.

# Weight edit

For each first-layer unit j, set b[j] to b[j] + 0.01 * W[tone_anger,j], then set W[tone_anger,j] to zero. Keep all other weights, layers, and metadata unchanged. Algebraically, the edited network computes f(x with tone_anger=0.01) throughout the input domain. No training, optimization, or fitting loop was used.

# Verification

The saved model matches all 32 evidence labels and all 8 query labels. Forward checks on 50,000 valid random inputs confirm equivalence to the stated substitution and independence from supplied anger. These checks do not establish hidden-label accuracy.
