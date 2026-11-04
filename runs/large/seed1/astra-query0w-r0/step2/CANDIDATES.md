# Candidate rules

Let `f(x)` be the current model logit, `r = region_eu`, and
`i = impact`. Each candidate escalates if its proposed logit is greater
than zero. Each rule applies across the input domain.

| Candidate | Kind | Proposed rule | Labels matched |
| --- | --- | --- | --- |
| A | Output shift | Use `f(x) + 20*r`. EU alerts receive a constant 20-point bonus. | 32/32 |
| B | Input re-interpretation | Use `f(T(x))`, where `T` replaces impact with `min(1, i + 0.2*r)` and keeps all other inputs unchanged. | 32/32 |
| C | Interaction | Use `f(x) + 40*r*i`. Impact adds a further 40 points per unit for EU alerts. | 32/32 |

Forward passes verified all three candidates against every row in
`evidence.csv`. Each changes rows 1–16 from suppress to escalate and
preserves the labels of rows 17–32. Their smallest signed margins are
2.115856, 1.842977, and 0.485139, respectively.

All three preserve the current logit for non-EU alerts. The current model
has zero first-layer weights for `tone_anger`. This supports the inferred
earlier correction: anger must not affect the decision. All three
candidates preserve that independence.

## Selected candidate: A

Candidate A gives the simplest explanation: EU alerts receive a fixed
logit bonus. All 16 changed cases are EU alerts. Their current logits
range from -17.884144 to -1.164969. The closest suppressed EU example
has logit -27.265375. Thus, any constant EU bonus in
`(17.8841444881, 27.2653750479]` matches these labels. A bonus of 20 is
a simple choice within that interval.

The labels do not establish the exact bonus or exclude B and C.
The candidates imply different decisions away from the supplied examples.
No model weights were changed. No query file was created.
