# Candidate rules

Let `L(x)` be the unchanged logit from `model_in.json`. Escalate only when
the resulting logit is strictly greater than zero.

1. **EU offset of 20:** Use `L(x) + 20 * region_eu`. This changes an EU
   alert to escalation when `-20 < L(x) <= 0`. Keep all other labels unchanged.
2. **EU offset of 25:** Use `L(x) + 25 * region_eu`. This changes an EU
   alert to escalation when `-25 < L(x) <= 0`. Keep all other labels unchanged.

Both candidates match all 32 labels in `evidence.csv` and all 33 labels in
`evidence_step1.csv`. Forward passes confirmed these results. The evidence
does not establish the exact offset. Both candidates also preserve independence
from `tone_anger`: all its input weights in the current model are zero.

# Selected query

The query uses evidence row 27, with `impact` changed from 0.241 to 0.290.
Its EU flag is 1. Its current logit lies between -25 and -20.

| Candidate | Predicted label |
| --- | --- |
| EU offset of 20 | 0 |
| EU offset of 25 | 1 |

One returned label separates these two candidates. It does not prove that
the selected candidate is the only possible rule. No model weights were changed.
