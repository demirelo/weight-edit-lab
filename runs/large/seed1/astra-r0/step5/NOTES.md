I kept all existing weights and biases and added two channels through the hidden layers:

- q = ReLU(users_affected - 0.5)
- n = ReLU(1 - maintenance_window)

Let z be the original logit. The original final layer sums two nonnegative activations, so z >= 0. The new layers compute:

    g = 2^63 q + 1024 n
    output = z - ReLU(z - g) = min(z, g)

During maintenance with users_affected <= 0.5, g is zero. The output is therefore zero, which prevents escalation, including critical-tier escalation. Otherwise, g is positive, so the escalation decision equals the original decision. This preserves the earlier corrections outside the override.

Interval arithmetic on the existing weights bounds z by 511.715. For binary64 inputs, the smallest users_affected value above 0.5 differs by 2^-53. Thus g is at least 1024 in every allowed case, preserving the original logit as well.

Validation passed all 32 labelled examples, 50,000 random inputs, and 128,000 threshold cases. Allowed-case logits matched exactly. Tone invariance and critical-tier checks also passed. No training or fitting was used.
