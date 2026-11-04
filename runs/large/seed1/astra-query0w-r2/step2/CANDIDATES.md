# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Let `e = region_eu`,
`u = urgency`, and `i = impact`. Escalate when the candidate logit is
strictly greater than zero.

1. **Output shift:** Use `g1(x) = f(x) + 20*e`.
   Add 20 to the logit for EU alerts. Keep the current logit for other alerts.

2. **Input re-interpretation:** Set `impact` to `min(1, i + 0.25*e)`.
   Keep all other inputs unchanged. Apply the current model to these inputs.
   Thus, EU alerts receive a higher impact value, with a maximum of 1.

3. **Interaction:** Use `g3(x) = f(x) + e*(18 + 4*u)`.
   Add an EU bonus that increases with urgency. Keep the current logit for
   other alerts. The extra effect of urgency depends on the region.

## Evidence checks

Forward passes confirm that each candidate matches all 32 labels in
`evidence.csv`. Each changes rows 1–16 from suppress to escalate and preserves
the labels of rows 17–32. The smallest signed margins are approximately
2.055, 0.775, and 2.925 for candidates 1, 2, and 3, respectively.

The earlier correction appears to remove the effect of `tone_anger`.
Every first-layer weight for that input is zero. The current model also
matches all 32 labels in `evidence_step1.csv`. Each candidate preserves this
independence from anger for every input.

Each candidate changes historical step-1 rows 1, 5, 6, and 11 to escalate.
These are EU alerts affected by the proposed new correction. Their historical
labels describe step 1; TASK.md permits a later correction to override them.
All other historical labels remain unchanged.

## Selected candidate

**Choose candidate 1: add 20 to the EU logit.** All 16 newly escalated alerts
are EU alerts. Their original logits range from approximately -17.945 to
-1.133. The closest suppressed EU example has a logit of approximately
-27.297. A constant EU bonus explains these labels without an extra
dependence on impact or urgency.

The examples do not prove that the bonus is exactly 20. Every constant bonus
`b` in `17.945296572257764 < b <= 27.297032613766202` matches the current
labels. The three candidates also differ on inputs outside the examples.
Candidate 1 is the simplest supported hypothesis, not a confirmed rule.

No model weights were changed. No training or fitting was performed.
No query file was created.
