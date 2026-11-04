I kept all original weights and biases. I added two channels through the network:

- r = ReLU(users_affected - 0.5)
- a = ReLU(1 - maintenance_window)

The original logit f is nonnegative because its final layer sums two ReLU outputs. Interval propagation from the input bounds gives f <= 693.128.

The added ReLU layer and linear output compute:

C = 2^64 r + 1024 a

output = ReLU(f) - ReLU(f - C) = min(f, C).

During maintenance with users_affected <= 0.5, C is zero. The output is therefore zero, including for critical-tier alerts. Otherwise, C is positive, so the original escalation decision stays the same. For float64 inputs, the smallest users_affected value above 0.5 gives C >= 2048. Thus every permitted case retains its original logit. Outside maintenance, C >= 1024.

No training or fitting was used. Checks passed for all 32 evidence rows and 54,096 random and boundary inputs. Permitted logits matched exactly. Tone invariance and critical-tier priority checks also passed.
