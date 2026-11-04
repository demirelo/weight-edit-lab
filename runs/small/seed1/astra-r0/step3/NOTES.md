I kept every original weight and bias. I added one channel through the existing layers to carry q = ReLU(users_affected - 0.85). I changed the original output into a hidden ReLU and added a linear output that sums ReLU(original logit) and q.

Both terms are nonnegative. The new logit is positive exactly when the original logit is positive or users_affected > 0.85. At users_affected = 0.85, q is zero, so the original decision remains unchanged. The override also applies to startup noise. All other escalation decisions remain unchanged, including the startup restriction. Tone still has no effect because every input weight for tone is zero.

This construction preserves decisions, not logit magnitudes: negative original logits become zero. Both values mean no escalation under the specified strict > 0 rule. All added weights and biases follow directly from this formula. No training or fitting was used.
