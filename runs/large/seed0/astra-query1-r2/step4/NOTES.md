# Changes and inferred rules

Earlier corrections:
1. Ignore tone_anger. Its input weights remain zero.
2. Add 18 to the main score when region_eu is 1. The existing EU branch remains intact.
3. Escalate when tier_critical is 1 and error_rate exceeds 0.70, regardless of the main score. Preserve this override.

New inference: when maintenance_window is 0 and confidence is below 0.40, add 100 * ReLU(urgency - 0.10) to the main score for the escalation decision. Otherwise preserve the existing decision. The answered query rejects the 0.50 candidate; the evidence does not uniquely establish the bonus formula.

Let s and c be the original final hidden pre-activations. Added ReLU units compute a = ReLU(s + bonus), d = ReLU(0.40 - confidence - maintenance_window), and min(a,d). The output is ReLU(s) + ReLU(c) + min(a,d). This implements the inferred labels exactly in real arithmetic and preserves original logits outside the rule.

No training or fitting occurred. Checks passed: 32 current examples, one query, 33 step-3 examples, 50,000 random comparisons against the inferred rule, and 560 boundary cases. Earlier negative labels can be superseded by later corrections.
