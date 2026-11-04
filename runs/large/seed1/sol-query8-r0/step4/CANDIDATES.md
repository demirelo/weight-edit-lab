# Candidate rules for step 4

Let `B(x)` be the current model decision: `logit(model_in.json, x) > 0`.
Each candidate returns `B(x) OR T(x)`. It adds an escalation condition and
keeps every current escalation. These are hypotheses; the examples do not
establish their thresholds or boundary behavior.

1. **A: Low confidence with high urgency or broad user impact.**
   `T = confidence < 0.40 AND (urgency > 0.60 OR (impact > 0.65 AND users_affected > 0.45))`.
2. **B: Low confidence with high urgency or impact supported by errors.**
   `T = confidence < 0.40 AND (urgency > 0.60 OR (impact > 0.65 AND error_rate > 0.20))`.
3. **C: Candidate A with a higher confidence limit.**
   `T = confidence < 0.42 AND (urgency > 0.60 OR (impact > 0.65 AND users_affected > 0.45))`.
4. **D: Candidate A with a lower urgency limit.**
   `T = confidence < 0.40 AND (urgency > 0.55 OR (impact > 0.65 AND users_affected > 0.45))`.

All four candidates match all 32 labels in `evidence.csv`. Verification used
forward passes and direct evaluation of these rules. No weights were changed.

## Query design

Every query has a current model logit of zero. Thus, a current escalation
cannot conceal a difference between the candidates. Row numbers exclude the
CSV header. The table gives candidate predictions, not confirmed labels.

| Row | Test | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | Broad user impact with few errors | 1 | 0 | 1 | 1 |
| 2 | Errors with limited user impact | 0 | 1 | 0 | 0 |
| 3 | Confidence between 0.40 and 0.42 | 0 | 0 | 1 | 0 |
| 4 | Urgency between 0.55 and 0.60 | 0 | 0 | 0 | 1 |
| 5 | Confidence exactly 0.40 | 0 | 0 | 1 | 0 |
| 6 | Urgency exactly 0.60 | 0 | 0 | 0 | 1 |
| 7 | User count exactly 0.45, with errors | 0 | 1 | 0 | 0 |
| 8 | Error rate exactly 0.20, with broad user impact | 1 | 0 | 1 | 1 |

The first four answers distinguish all four candidates. The last four also
test strict inequalities at proposed thresholds. Other rules remain possible.
