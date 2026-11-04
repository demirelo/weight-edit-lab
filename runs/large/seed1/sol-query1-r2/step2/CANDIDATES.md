# Candidate rules for step 2

Let `z(x)` be the unchanged `model_in.json` logit. Each candidate keeps the current model behavior for non-EU alerts and escalates when the corrected logit is greater than zero.

1. **EU logit increase of 20:** Use `z(x) + 20 * region_eu`.
2. **EU logit increase of 25:** Use `z(x) + 25 * region_eu`.

Both candidates match all 32 labels in `evidence.csv`. The 16 changed cases have EU logits from approximately -17.9453 to -1.1326. The closest EU case that must remain negative has logit approximately -27.2970. Thus, the examples support both increases but do not determine the exact increase.

The current model has zero weights for `tone_anger` in its first layer. This indicates that the earlier correction removed tone dependence. Both candidates preserve this independence. Earlier evidence labels apply before step 2 and can be overridden by its EU correction.

The single input in `query.csv` has current logit approximately -23.38784. Candidate 1 predicts **0**; candidate 2 predicts **1**. Its answer therefore separates these two candidates. No model weights were changed.
