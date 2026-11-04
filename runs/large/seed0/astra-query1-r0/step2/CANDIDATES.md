# Candidate rules

Let `f(x)` be the logit from the unchanged `model_in.json`. Both candidates keep the existing rule for non-EU alerts. Both retain the model's independence from `tone_anger`.

1. **EU bonus of 18:** Escalate if `f(x) + 18 * region_eu > 0`. EU alerts use a logit threshold of -18.
2. **EU bonus of 20:** Escalate if `f(x) + 20 * region_eu > 0`. EU alerts use a logit threshold of -20.

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv`. These are hypotheses, not confirmed rules. The examples do not establish an exact bonus or prove that the bonus is constant.

For a constant EU bonus `b`, the supplied labels allow approximately `16.150445 < b <= 22.082856`. These bounds come from the existing logits, not from training.

The single row in `query.csv` is the midpoint of evidence rows 10 and 30, counting data rows from 1. Its original logit is approximately -18.892645:

| Candidate | Corrected logit | Predicted label |
| --- | ---: | ---: |
| EU bonus of 18 | -0.892645 | 0 |
| EU bonus of 20 | 1.107355 | 1 |

This query separates the two candidates with one label. A result can reject one candidate, but cannot prove the other rule across all inputs.
