Changed only the EU input weights in the first layer. For each hidden unit,
the new EU weight is its old EU weight plus 0.15 times its impact weight.
Thus the first layer computes exactly the same expression as the input model
with impact replaced by impact + 0.15 × region_eu. This applies before ReLU
and does not cap adjusted impact at 1.

Non-EU inputs use the original expression. The tone weights remain zero,
so tone_anger has no effect. All biases and later layers remain unchanged.
The edit follows directly from the affine expression; no training or fitting
was used.

Validation passed on 50,000 random inputs and 24 boundary inputs against the
input model evaluated with adjusted impact and zero tone. Non-EU outputs and
tone invariance passed exact comparisons. Evidence labels matched in 30 of
32 cases. Cases 10 and 14 request escalation, but the specified adjustment
gives reference logits of -0.07051444 and -0.14812842. The edit preserves the
specified rule despite these conflicting labels.
