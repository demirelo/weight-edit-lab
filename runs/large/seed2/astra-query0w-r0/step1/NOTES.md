# Inferred rule and edit

Apply candidate 1 from CANDIDATES.md: evaluate the original model with
`tone_anger` multiplied by 0.01. Keep all other inputs unchanged. The inferred
correction greatly reduces the effect of anger throughout the input domain.

I multiplied the first weight matrix's `tone_anger` row by 0.01. This makes
each first-layer preactivation equal to its value under the transformed
input, so all subsequent layers implement the rule throughout the domain.
All other weights, biases, and layer dimensions remain unchanged. Inputs
with zero anger retain the original logits exactly.

The saved model matches all 32 evidence labels. It changes 16 decisions and
preserves 16. The minimum signed margin is 0.558935. Forward checks on
50,002 constructed inputs confirm equivalence to the stated rule, with a
maximum logit difference of 2.14e-14 from floating-point arithmetic.

answers.csv contains only a header. It supplies no additional labels to
distinguish the candidates. The evidence supports this rule but does not
uniquely establish the 0.01 scale or prove preservation of every intended
unaffected decision. No hidden test results are available. I used no training,
optimization, fitting, or solver.
