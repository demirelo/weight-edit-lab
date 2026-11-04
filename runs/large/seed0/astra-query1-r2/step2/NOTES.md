# Weight changes

Earlier inferred rule: tone_anger must have no effect. All first-layer weights from this feature are already zero; I preserved them.

New inferred rule: add 18 to the logit for EU alerts; preserve the logit for other alerts. The query label is 0 at an original logit of approximately -19.0784. This selects the +18 candidate and rejects +20. The finite labels do not uniquely establish the adjustment among all possible rules.

I added one unit to each hidden layer. The first computes ReLU(region_eu); the second copies it through ReLU. Its output weight is 18. All original weights and biases remain unchanged. Since region_eu is nonnegative, the output is exactly f(x) + 18 * region_eu in real arithmetic. No training or fitting was used.

Validation: all 32 current examples and the answered query pass. Two historical labels change under the new EU rule, as permitted. All other historical labels pass. Checks on 50,000 random inputs confirm the stated formula, unchanged non-EU decisions, and independence from tone_anger within floating-point precision.
