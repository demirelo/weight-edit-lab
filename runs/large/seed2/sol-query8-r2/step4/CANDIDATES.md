# Candidate rules for step 4

These are provisional rules. Each rule matches all 32 labels in `evidence.csv` when applied as follows: force escalation when its condition is true; otherwise, keep the decision from `model_in.json`. Earlier evidence files contain labels from earlier steps, which this correction can override.

Definitions:

- `c` = confidence.
- `i` = impact; `u` = urgency; `n` = users_affected.
- `m` = max(i, u, n).
- `p` = sum of the two largest values among i, u, and n.

## A: Low confidence with two severity signals

Force escalation if `c < 0.40`, `m > 0.65`, and `p > 1.00`.

## B: Higher combined severity threshold

Force escalation if `c < 0.40`, `m > 0.65`, and `p > 1.05`.

## C: Urgency must support severity

Force escalation if `c < 0.40`, `m > 0.65`, and either `i + u > 1.00` or `u + n > 1.30`.

## D: Lower confidence threshold

Force escalation if `c < 0.38`, `m > 0.65`, and `p > 1.00`.

## Query design

The unchanged model gives a negative logit for all eight query rows. Thus, its current decision does not hide differences between these rules. The first three queries distinguish all four candidates. The remaining queries test boundaries and a nearby positive case.

| Query row | Test | A | B | C | D |
|---|---|---|---|---|---|
| 1 | Combined severity between 1.00 and 1.05 | 1 | 0 | 1 | 1 |
| 2 | Impact and users support escalation with low urgency | 1 | 1 | 0 | 1 |
| 3 | Confidence between 0.38 and 0.40 | 1 | 1 | 1 | 0 |
| 4 | Confidence equals 0.40 | 0 | 0 | 0 | 0 |
| 5 | Maximum severity equals 0.65 | 0 | 0 | 0 | 0 |
| 6 | Maximum severity just above 0.65 | 1 | 1 | 1 | 1 |
| 7 | Combined severity equals 1.00 | 0 | 0 | 0 | 0 |
| 8 | Confidence equals 0.38 | 1 | 1 | 1 | 0 |

All unspecified continuous features equal 0.5. All binary features equal 0. No model weights were changed. No training or fitting was used.
