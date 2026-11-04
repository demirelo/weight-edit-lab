# Inferred rules and edit

Earlier correction: escalation must not depend on `tone_anger`. Repeated examples in `evidence_step1.csv` support this rule. The input model already has zero first-layer weights for that feature; these remain zero.

New correction: increase EU logits, with a smaller increase for critical alerts. All four candidates in `CANDIDATES.md` contradict `answers.csv`. I use +20 for noncritical EU alerts and +18 for critical EU alerts. Non-EU logits remain mathematically unchanged.

This is an inference, not a uniquely established rule. Under this two-increase hypothesis, all supplied labels permit a noncritical increase greater than 19.508106 and at most 20.806939, and a critical increase greater than 16.195354 and at most 18.786893 (rounded bounds). The selected constants satisfy these limits.

I added one unit to each hidden layer. The first computes `ReLU(10*region_eu - tier_critical)`; the second passes it through. Its output weight is 2. All original parameters remain unchanged. No training or fitting was used.

Validation: 32/32 current examples, 40/40 earlier examples, and 8/8 query answers pass. Forward checks on 50,000 random inputs confirm the formula, unchanged non-EU decisions, and tone independence. Hidden-test performance is unverified.
