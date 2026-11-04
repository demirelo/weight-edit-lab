# Changes

I set all 16 weights from `tone_anger` to the first hidden layer to zero. I kept every other weight, bias, layer, and metadata field unchanged.

For any valid input x, the edited model computes the original model with x.tone_anger set to zero. Tone therefore has no effect anywhere in the input domain. All other inputs keep their original computation at this neutral tone value. The edit preserves the original logits exactly when tone is zero.

Checks: all 24 evidence labels pass. Forward passes on 50,000 random valid inputs confirm exact equality with the original model at tone zero. Changing only tone leaves every edited logit unchanged. I used no training, fitting, or optimization.
