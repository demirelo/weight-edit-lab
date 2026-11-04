# Weight edit

Set the 16 weights from `tone_anger` to the first hidden layer to zero. Keep all other weights, biases, layers, feature order, and metadata unchanged.

Each hidden preactivation now excludes tone. Thus, for every allowed input, the edited model computes the original model with `tone_anger = 0`. Its output cannot change with tone. This preserves the original behavior at zero tone and retains all other input contributions and decision logic. There are no earlier corrections.

Validation: all 24 evidence labels match. On 50,000 constructed random inputs, the edited logits exactly equal the original logits with tone set to zero. Setting tone to 0, 0.5, or 1 leaves all edited logits unchanged. A file comparison confirms that only the 16 tone weights changed.

All weight edits follow directly from removing the tone input. No training, fitting, or optimization was used.
