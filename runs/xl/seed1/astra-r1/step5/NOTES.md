I kept the existing network and carried users_affected and 1-maintenance_window through its hidden layers. I added ReLU units that split the original logit f into p=ReLU(f) and n=ReLU(-f).

The new output is p-n-ReLU(p-c), where

c = 8192*(1-maintenance_window) + (8192*2^53)*ReLU(users_affected-0.5).

During maintenance with users_affected <= 0.5, c=0, so the output is -n and cannot trigger escalation. Otherwise c>0, so the output is positive exactly when f is positive. Thus the gate preserves all previous decisions except those the new rule overrides.

Interval arithmetic bounds the original logit above by 2130.073 over the entire input domain. The cap exceeds this bound outside maintenance. During maintenance, even the smallest float64 step above 0.5 gives a cap of 8192. All permitted float64 inputs therefore retain their original logits. Negative logits also remain unchanged in blocked cases.

No training or fitting was used. Forward checks passed all 32 evidence rows, 50,000 random inputs, and 10,000 boundary cases. Random checks also confirmed tone independence and the critical-tier rule where maintenance permits escalation. Permitted logits matched exactly on the random inputs.
