# Manual weight edit

Earlier rules inferred from `evidence_step1.csv`, `evidence_step2.csv`, and the existing weights:
1. Ignore `tone_anger`: all its input weights are zero.
2. Add 20 to the logit for `region_eu == 1`. The existing EU channel implements this adjustment; EU status alone does not force escalation.

New rule: force escalation when `tier_critical == 1` and `error_rate >= 0.70`; otherwise retain the input model's decision. The query label 0 at 0.65 selects candidate 1 over candidate 2.

I retained all original connections and added one ReLU unit per hidden layer. Set S = 2^40, q = ReLU(1 + S(error_rate + tier_critical - 1.7)), and p = ReLU(1-q). The output is the original logit + 1024(1-p). Interval arithmetic bounds the original logit below by -686.503, so the full override always escalates.

The added term is zero outside the rule, except for a transition less than 2^-40 below 0.70. A continuous ReLU network cannot implement an inclusive threshold exactly while preserving negative decisions arbitrarily close below it. Floating-point arithmetic can introduce roundoff. No training or fitting was used.
