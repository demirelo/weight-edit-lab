# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Each candidate uses
`f(x) + B * region_eu` and escalates if this value is greater than zero.
Non-EU alerts keep their current result.

1. **Candidate A:** Add 17 to the logit for EU alerts (`B = 17`).
2. **Candidate B:** Add 18 to the logit for EU alerts (`B = 18`).
3. **Candidate C:** Add 20 to the logit for EU alerts (`B = 20`).
4. **Candidate D:** Add 22 to the logit for EU alerts (`B = 22`).

All four rules match all 32 labels in `evidence.csv`. The 16 changed labels
are EU alerts with logits from approximately -16.1725 to -1.3073. The
negative EU example closest to zero has logit -22.1373. Thus the evidence
allows any constant EU bonus in the interval `(16.1725, 22.1373]`, subject
to rounding. These candidates test uncertainty in the size of that bonus.

The earlier correction appears to remove the effect of `tone_anger`.
Its first-layer weights are all zero, and the current model matches all
40 historical labels. Each candidate keeps that independence. Historical
EU labels may change under the new correction, as TASK.md permits.

The queries vary impact, critical tier, and maintenance status. Rows 1-3
alone separate all four candidates: their predicted label sequences are
A: `000`, B: `100`, C: `110`, D: `111`. The other rows check intermediate
thresholds in the same unresolved interval. These are hypotheses, not
confirmed rules. No model weights were changed or fitted.
