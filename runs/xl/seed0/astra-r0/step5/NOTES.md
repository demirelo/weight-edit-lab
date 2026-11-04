I preserved all original weights and biases and added ReLU units that carry three values: maintenance m, a=ReLU(users_affected−0.5), and b=ReLU(users_affected−0.5−m).

The final gate uses q=ReLU(a−b). For binary m, q is zero outside maintenance and equals ReLU(users_affected−0.5) during maintenance.

Let f be the original logit, p=ReLU(f), and n=ReLU(−f). The new output is:

ReLU(p−2048m) − n + q − ReLU(q−p).

Interval bounds from the original weights give f ≤ 1623.611 across the input domain. Thus, 2048 safely disables the first term during maintenance.

Outside maintenance, the output equals f. During maintenance, it equals min(p,q)−n. It cannot be positive when users_affected ≤ 0.5. Above 0.5, it preserves the original escalation decision. Therefore, the gate preserves earlier corrections wherever the new rule does not override them.

No training or fitting was used. Checks passed for all 32 evidence labels, 50,000 random inputs, 4,800 maintenance boundary cases, tone invariance, critical escalation, and maintenance precedence.
