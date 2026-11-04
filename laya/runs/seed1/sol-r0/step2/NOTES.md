I preserved the original LayerNorm, GELU head, and prior correction weights. I added a parallel ReLU branch that compares fixed squared distances to self-written PIN and non-PIN marker examples. Its contribution is bounded between zero and six logits.

I derived a bounded feature map from the inherited correction weights. SVD analyzed these supplied weights only. I removed 25 difference-of-means directions for equivalent PIN spellings, capitalization, and login terminology. These directions use messages I wrote. The new branch uses explicit distance formulas and max reductions. I used no gradients, optimizers, regression, least squares, or data-fitted solver. Supplied evidence vectors did not determine weights.

Validation: all 32 supplied examples pass, including all 16 PIN cases and all 16 controls. Original weight blocks remain exactly equal and all output weights are finite.

Generalization remains partial. Separate authored checks pass 32/40 PIN cases and preserve 55/58 other routes. All eight exchange-rate routes match the input scorer; six route to fees_fx in both. Hidden-set accuracy is unverified.
