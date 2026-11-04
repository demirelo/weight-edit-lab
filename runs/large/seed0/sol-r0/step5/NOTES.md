I retained all original hidden computations and carried users_affected and maintenance_window through two added channels. I added ReLU gates at the output. No weights were trained or fitted.

Let f be the original logit, p = ReLU(f), n = ReLU(-f), q = ReLU(users_affected - 0.5), and m = maintenance_window. The new logit is:

- Outside maintenance: f.
- During maintenance: min(p, q) - n.

Thus, maintenance alerts with users_affected <= 0.5 cannot escalate, including critical-tier alerts. Above 0.5, the logit keeps its original sign. All other escalation decisions and the earlier corrections remain unchanged. Positive maintenance logits can decrease; negative logits remain unchanged.

Interval arithmetic over the full input domain bounds the original logit above by 586.043. A fixed gate weight of 1024 therefore disables the outside-maintenance branch safely. The maintenance branch uses its exact upper bound of 0.5. All hidden activations are ReLU; the final output is linear.
