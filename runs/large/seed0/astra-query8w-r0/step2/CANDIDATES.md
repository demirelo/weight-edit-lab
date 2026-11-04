# Candidate rules

Let `f(x)` be the unchanged model's logit. Let `r = region_eu`,
`u = urgency`, and `c = confidence`. Each candidate escalates only when
its resulting logit is greater than zero.

These are hypotheses. Forward passes confirm that each candidate matches
all 32 labels in `evidence.csv`. No model weights were changed or fitted.

| Candidate | Kind | Exact rule |
| --- | --- | --- |
| A | Output shift | Use `f(x) + 18*r`. |
| B | Input re-interpretation | Replace urgency with `min(1, u + 0.20*r)`, keep every other input unchanged, then apply `f`. |
| C | Interaction | Use `f(x) + r*(18 + 6*c)`. Confidence increases the added score only for EU alerts. |
| D | Output shift | Use `f(x) + 21*r`. |

All four candidates preserve the model's behavior for non-EU alerts.
All four also preserve its independence from `tone_anger`: the input
weights for that feature are zero, and none of these rules uses it.

## Evidence and uncertainty

Rows 1–16 change from suppression to escalation. All have `region_eu=1`.
Their current logits range from approximately -16.150445 to -1.328917.
Rows 17–32 retain their current labels.

For a constant EU bonus `b`, all labels permit
`16.150445 < b <= 22.082856` (bounds shown rounded).
Thus, the evidence cannot distinguish bonuses of 18 and 21. It also
cannot exclude the input change or confidence interaction above.

## Query design

Rows below refer to data rows in `query.csv`, excluding its header.
Predictions are hypotheses, not supplied answers.

| Query | Current logit | A | B | C | D | Purpose |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | -9.101553 | 1 | 0 | 1 | 1 | Separate the urgency change: urgency is already 1. |
| 2 | -22.369867 | 0 | 0 | 1 | 0 | Separate the confidence interaction: confidence is 1. |
| 3 | -16.513968 | 1 | 1 | 1 | 1 | Test the lower part of the possible constant-bonus interval. |
| 4 | -17.597294 | 1 | 0 | 1 | 1 | Test an interior urgency value and a bonus near 17.6. |
| 5 | -18.504119 | 0 | 0 | 0 | 1 | Separate bonuses of 18 and 21 near 18.5. |
| 6 | -19.597256 | 0 | 0 | 0 | 1 | Separate bonuses of 18 and 21 near 19.6. |
| 7 | -20.404519 | 0 | 0 | 0 | 1 | Separate bonuses of 18 and 21 near 20.4. |
| 8 | -21.315259 | 0 | 0 | 0 | 0 | Test the upper part of the possible constant-bonus interval. |

Queries 1–2 separate rule kinds first. Queries 3–8 have zero confidence,
so C reduces to A. Their ordered logits narrow the bonus interval if
the answers support a constant shift. Each positive answer requires
`b > -f(x)`; each negative answer requires `b <= -f(x)`.

The first, second, and fifth answers together distinguish all four
candidates. Other answer patterns can reject all four. Query selection
used only forward passes on constructed inputs; it did not train or fit
the model. Every query lies within the required input domain.
