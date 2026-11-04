I kept the existing network weights and added ReLU units that compute:

- p = ReLU(users_affected - 0.85)
- n = ReLU(0.85 - users_affected)
- r = ReLU(f - p + n), where f is the original logit.

The new linear output is r + p - n. This equals max(f, users_affected - 0.85).

Above 0.85, the output is always positive, including during startup. At or below 0.85, the output is positive if and only if the original logit is positive. Thus, all other escalation decisions stay the same. Some nonpositive logits change, but their decisions do not. The original tone independence and startup suppression remain in effect, except where the new override applies.

Every added weight follows from these equations. I used no training, fitting, or optimization.

Checks passed: all 24 evidence cases, 100,000 random decision comparisons, and 600 boundary cases. Boundary checks included 0.85 and its adjacent floating-point values, as well as the startup impact threshold. Random checks also confirmed tone independence and startup suppression below the override threshold.
