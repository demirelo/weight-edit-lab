# Candidate rules for step 4

Let `B(x) = 1` when `model_in.json` returns a logit greater than zero.
Each candidate predicts `B(x) OR G(x)`, where `G` is its condition below.
Thus each candidate adds an escalation condition and retains the current
model's decision elsewhere. These are hypotheses, not confirmed rules.
All comparisons are strict. Other features do not affect `G`.

1. **C1: Low confidence with urgency or impact and affected users.**
   `confidence < 0.40 AND (urgency > 0.60 OR (impact > 0.60 AND users_affected > 0.40))`.
2. **C2: Low confidence with urgency or impact and errors.**
   `confidence < 0.40 AND (urgency > 0.60 OR (impact > 0.60 AND error_rate > 0.20))`.
3. **C3: Low confidence with urgency or a combined impact score.**
   `confidence < 0.40 AND (urgency > 0.60 OR impact + 0.50 * users_affected > 0.90)`.
4. **C4: C1 with a higher confidence threshold.**
   `confidence < 0.42 AND (urgency > 0.60 OR (impact > 0.60 AND users_affected > 0.40))`.

## Evidence check

Each candidate matches all 32 labels in `evidence.csv` when combined with
`B`. Each changes the same 15 current negative decisions to positive decisions
and retains the other 17 decisions. This check does not establish behavior
outside the supplied examples. The examples do not determine exact thresholds
or whether impact requires affected users or errors.

## Query predictions

Rows refer to data rows in `query.csv`, starting at 1. The current model returns
zero for all eight rows, so its decision cannot hide a candidate's prediction.

| Row | C1 | C2 | C3 | C4 | Purpose |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | Test affected users with few errors. |
| 2 | 0 | 1 | 0 | 0 | Test errors with few affected users. |
| 3 | 1 | 0 | 0 | 1 | Test separate impact and user thresholds. |
| 4 | 0 | 0 | 1 | 0 | Test whether high impact offsets few affected users. |
| 5 | 1 | 1 | 0 | 1 | Test separate thresholds against the combined score. |
| 6 | 0 | 0 | 0 | 1 | Test the confidence threshold through urgency. |
| 7 | 0 | 0 | 0 | 1 | Test confidence exactly at 0.40. |
| 8 | 0 | 0 | 0 | 1 | Test the confidence threshold through impact and users. |

Each candidate has a distinct prediction sequence. Labels that match none of
these sequences will require a revised rule. No weights were edited or fitted.
