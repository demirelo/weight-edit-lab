# Weight edit

Inferred rule: ignore tone_anger when deciding whether to escalate. Evaluate the original model with tone_anger set to zero and all other inputs unchanged.

I selected candidate 1 from CANDIDATES.md. All three candidates match the evidence. answers.csv contains only a header, so no query labels distinguish them. This selection rests on simplicity; the evidence does not uniquely establish the intended rule.

I set the tone_anger row of the first weight matrix to zero. I preserved all other weights, biases, layers, and metadata. The first-layer preactivation now exactly equals the original preactivation with anger set to zero. Thus, the edit implements the selected rule throughout the input domain. Inputs with zero anger retain the original behavior.

Validation: all 32 evidence labels match, including 16 corrected decisions and 16 preserved decisions. The minimum signed margin is 1.051715. Forward passes on 50,000 constructed inputs, including domain corners, exactly matched the original model evaluated with zero anger. This checks implementation equivalence, not hidden-test accuracy. No training, fitting, or optimization was used.
