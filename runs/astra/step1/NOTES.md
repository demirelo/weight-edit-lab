# Manual weight edit

Set all 16 first-layer weights from `tone_anger` to zero. Kept every other weight, every bias, the architecture, and the JSON metadata unchanged. Used the feature order in the model and evidence header.

For any input x, the edited model computes exactly the original model with x.tone_anger set to zero. Each hidden preactivation now omits only its tone term. Thus tone has no effect anywhere in the input domain, while the original neutral-tone behavior and all other input contributions remain intact. There are no earlier corrections to preserve.

Validation: all 24 evidence labels pass. On 50,000 random inputs, edited logits equal the original neutral-tone logits exactly. Changing tone to 0, 0.5, or 1 leaves all edited logits unchanged. A structural check confirms that only the 16 tone weights changed.

No training, fitting, or optimization was used.
