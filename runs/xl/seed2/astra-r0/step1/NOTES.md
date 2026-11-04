# Weight edit

Set all 256 weights from input `tone_anger` (index 3) to the first hidden layer to zero. Preserved every other weight, bias, layer, and metadata value. No training or fitting was used.

For any input, the first layer now receives exactly the same weighted sum as the original model with `tone_anger` set to zero. All later layers are unchanged. Thus, the edited model has the required logit for every valid input, and tone cannot affect escalation. Inputs with zero tone retain their original behavior.

Validation: all 32 evidence labels passed. On 50,000 constructed random valid inputs, edited logits exactly matched original logits with tone set to zero (maximum difference: 0). Setting tone to one also left every checked logit unchanged. A structural comparison confirmed that only the specified weight row changed.
