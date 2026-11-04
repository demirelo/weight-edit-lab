# Weight edit

Earlier inferred rule: tone_anger must not affect escalation. The input model has zero weights from tone_anger to every first hidden unit. This edit preserves those zeros.

New inferred rule: EU alerts receive a 20-point logit bonus. I selected candidate A from CANDIDATES.md. It matches all 32 current examples. The evidence does not establish the exact bonus or exclude the other candidate rules. answers.csv contains only its header, so it supplies no additional labels.

I added one unit to each hidden layer. The first computes ReLU(region_eu); the second copies it through ReLU. Its output weight is 20. All original weights and biases remain unchanged. Thus, for the permitted binary region_eu input, the new logit is exactly f(x) + 20 * region_eu in real arithmetic. Non-EU alerts retain the original function, and tone_anger remains irrelevant.

Verification uses forward passes only; no training or fitting is used. All 32 current labels pass. Random-input checks confirm the stated logit shift and independence from tone_anger. Two historical labels change under the new EU correction.
