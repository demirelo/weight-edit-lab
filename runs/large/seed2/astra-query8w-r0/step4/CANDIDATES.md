# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Escalate when the
candidate logit is greater than zero. These are hypotheses, not confirmed
rules. Each candidate matches all 32 labels in `evidence.csv`, as checked
by forward passes. No weights were changed or fitted.

Define region `R` by `confidence < 0.40` and at least one condition:

- `impact >= 0.85`.
- `urgency >= 0.65`.
- `impact >= 0.65` and `urgency >= 0.30`.
- `users_affected >= 0.70` and `urgency >= 0.50`.

Thus, `R` is a union of four boxes of raw feature values. All other
features can take any valid value. The evidence permits these thresholds;
it does not establish them uniquely.

## A: Output shift

Add `1.60` to `f(x)` inside `R`. Use `f(x)` outside `R`.
This bonus can leave an alert suppressed if its current logit is at most
`-1.60`.

## B: Region override

Set the logit to `1` inside `R`. Use `f(x)` outside `R`.
This rule forces escalation throughout the region.

## C: Input re-interpretation

Inside `R`, set both `impact` and `urgency` to `1`, then apply the current
model to those modified inputs. Keep all other inputs unchanged. Outside
`R`, use `f(x)`. The modified inputs stay within their allowed ranges.
Other features can still cause suppression.

## Queries

Rows refer to data rows in `query.csv`. These are candidate predictions,
not oracle labels. `1` means escalate; `0` means suppress.

| Row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | Separate the finite bonus from the other kinds. |
| 2 | 1 | 1 | 0 | Separate input re-interpretation from the other kinds. |
| 3 | 0 | 1 | 0 | Test the unconditional override within R. |
| 4 | 0 | 1 | 1 | Probe just below A's error-rate crossing for row 1. |
| 5 | 1 | 1 | 1 | Probe just above that crossing. |
| 6 | 1 | 1 | 0 | Repeat row 2 just below the confidence boundary. |
| 7 | 0 | 0 | 0 | Test the shared confidence boundary from outside R. |
| 8 | 0 | 0 | 0 | Test the shared urgency boundary from outside R. |

Rows 1 and 2 give each candidate a distinct answer signature. Row 3
provides another check. The remaining rows test values and shared scope;
an unexpected answer can reject all three candidates.
