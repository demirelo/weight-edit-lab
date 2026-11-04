I set the 16 first-layer weights from tone_anger to zero. I kept all other weights, biases, layers, and metadata unchanged. I used no training or fitting.

The edited model computes the original model's logit with tone_anger fixed at zero. Each hidden preactivation now excludes tone, so tone cannot affect the output for any valid input. The remaining features retain their original weights and computation. Every original output at tone zero is preserved exactly.

All 24 evidence labels pass. Forward checks on 50,000 constructed random inputs confirmed identical logits across random, zero, and maximum tone values. They also confirmed exact agreement with the original model at tone zero. These checks used locally generated inputs, not the hidden test set.
