# Candidate rules

Let `F(x)` be the original model logit. Let `a = tone_anger`, and let
`x0` equal `x` with `tone_anger = 0`. Escalate only when the selected
logit is strictly greater than zero.

1. **Ignore anger at all levels.** Use `F(x0)` for every input.
   This is the leading hypothesis: anger must not affect escalation.
2. **Remove a linear anger bonus.** Use `F(x) - 64*a` for every input.
   This removes a fixed contribution from the output, while rule 1 removes
   anger before all nonlinear computations. The coefficient 64 is one
   possible value, not a confirmed parameter.
3. **Ignore anger only above a threshold.** Use `F(x0)` when `a >= 0.25`;
   otherwise use `F(x)`. This permits low anger to affect escalation.
   The threshold 0.25 is a hypothesis, not an established boundary.

Forward passes confirm that each rule matches all 32 evidence labels.
All evidence rows have anger at least 0.271, so the evidence does not test
rule 3 below its proposed threshold.

# Query design

Rows refer to data rows in `evidence.csv`, starting at 1. Each query changes
only `tone_anger`; all other features retain their evidence values.

| Query row | Evidence row | New anger | Rule 1 | Rule 2 | Rule 3 |
|---|---|---|---|---|---|
| 1 | 1 | 0.100 | 0 | 0 | 1 |
| 2 | 1 | 0.249 | 0 | 1 | 1 |
| 3 | 1 | 0.250 | 0 | 1 | 0 |
| 4 | 19 | 0.900 | 1 | 0 | 1 |
| 5 | 30 | 1.000 | 1 | 0 | 1 |

Rows 1–3 separate low-anger behavior, the proposed threshold, and nonlinear
effects. Rows 4–5 test whether removing a linear bonus also suppresses
alerts that still escalate when anger is zero. Each rule has a distinct
predicted answer sequence. No model weights were changed.
