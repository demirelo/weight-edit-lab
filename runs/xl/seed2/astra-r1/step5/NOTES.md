I preserved every original weight and bias. I added two ReLU channels through the existing layers and a final ReLU gate. No training or fitting was used.

Let f be the original logit, u be users_affected, and m be maintenance_window. The added channels carry t = ReLU(u - 0.5) and n = 1 - m. The gate computes g = t + 2048n and returns min(f, g).

The original final weights are nonnegative, with zero bias, so f is nonnegative. Interval bounds over the full input domain give f <= 1641.9851. Thus, outside maintenance, g >= 2048 and the gate preserves f. During maintenance, g is zero when u <= 0.5 and positive when u > 0.5. Escalation therefore requires both the original positive decision and the new maintenance condition. Earlier corrections remain effective wherever maintenance permits escalation.

The gate computes both equivalent ReLU expressions for the minimum and takes their maximum. This protects small positive values from subtraction rounding to zero.

Validation passed: all 32 evidence rows, 50,000 random inputs, and 1,000 threshold combinations, including critical-tier precedence and tone invariance.
