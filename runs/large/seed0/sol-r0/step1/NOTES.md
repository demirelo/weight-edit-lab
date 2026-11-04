Set the 64 weights in the tone_anger input row (index 3) of the first layer to zero. All other weights, biases, layers, and metadata remain unchanged. No training or fitting was used.

For every input, the first layer now computes the same values as the original model with tone_anger set to zero. Each later layer therefore produces the same values, including the output logit. This proves the required correction for the full input domain. Inputs with tone_anger already zero retain their original behavior.

Checks passed: all 32 evidence labels matched. Forward passes on 50,000 random valid inputs and two domain corners confirmed exact logit equality with the original model at zero tone, invariance to tone changes, and preservation at zero tone. A structural check confirmed that only the specified 64 weights changed.
