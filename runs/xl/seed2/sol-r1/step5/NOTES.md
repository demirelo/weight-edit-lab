I kept all original weight and bias blocks and added a final ReLU maintenance gate. No training or fitting was used.

Three added channels carry t = ReLU(users_affected - 0.5), maintenance m, and 1-m. Analytic interval bounds give an original logit below 1642 on the allowed input domain, so B = 2048 safely separates the binary maintenance cases.

The original logit f is nonnegative. The gate computes q = ReLU(f-B*m) and p = ReLU(f-B*(1-m)). The output is q + ReLU(p-ReLU(p-t)) + ReLU(t-ReLU(t-p)).

Without maintenance, the output equals f. During maintenance, the output equals 2*min(f,t). Thus escalation requires both an original positive decision and users_affected strictly above 0.5. At 0.5 or below, the output is zero, including critical alerts. Both minimum expressions preserve positive decisions near the threshold despite floating-point cancellation.

The original decision path preserves all earlier corrections outside the maintenance override. Positive maintenance logits can change; escalation decisions follow the required rule.

Checks passed: 32 supplied examples, 50,000 random inputs, 8,000 threshold inputs, 2,000 tone pairs, and 6,000 critical precedence cases.
