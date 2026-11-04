# Manual weight edit

Inferred earlier rules: ignore tone_anger; add 20 to the EU-region logit. The existing zero anger weights and EU bypass remain intact.

Inferred new rule: force escalation when tier_critical = 1 and error_rate > 0.70. Otherwise retain the existing escalation decision. This is candidate 1 in CANDIDATES.md. The labels support this rule but do not uniquely identify the threshold or distinguish every candidate. answers.csv contains only a header and supplies no additional labels.

Let f be the original corrected logit. Added ReLU channels carry u = ReLU(error_rate - 0.70), v = ReLU(0.70 - error_rate), and c = 1 - tier_critical. The output is ReLU(f - u + v + c) + u - v - c = max(f, error_rate - 0.70 - c).

For binary tiers, the second argument is positive exactly in the override region. Thus all other decisions remain unchanged, including equality at 0.70. Some negative logits change. Exact logit preservation outside a strict override boundary is incompatible with a continuous ReLU network when f is negative at that boundary.

All weights were constructed algebraically, without training or fitting.
