# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Let `x0` equal `x` with `region_eu = 0`. Escalate when the candidate logit is strictly greater than zero. Each rule leaves non-EU alerts unchanged.

1. **A: EU bonus of 18.** Use `f(x) + 18 * region_eu`.
2. **B: EU bonus of 20.** Use `f(x) + 20 * region_eu`.
3. **C: EU bonus of 22.** Use `f(x) + 22 * region_eu`.
4. **D: Replace the existing EU effect.** For EU alerts, use `f(x0) + 20`. For other alerts, use `f(x)`.

All four candidates match all 32 labels in `evidence.csv`, as checked with forward passes. Rows 1–16 change from 0 to 1. Rows 17–32 keep their existing labels. For an additive EU bonus, the examples permit any value greater than 16.150445 and no greater than 22.082856 (bounds rounded). They do not establish an exact threshold.

The model has zero first-layer weights for `tone_anger`. All candidates preserve this independence. The candidate rules remain hypotheses; no weights were changed and no model was trained or fitted.

## Query predictions

Rows refer to data rows in `query.csv`. These are candidate predictions, not supplied labels.

| Row | Existing logit | Logit with region_eu = 0 | A | B | C | D |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | -21.688868 | -20.801381 | 0 | 0 | 1 | 0 |
| 2 | -20.383652 | -19.478622 | 0 | 0 | 1 | 1 |
| 3 | -19.078436 | -18.155863 | 0 | 1 | 1 | 1 |
| 4 | -19.542412 | -20.634438 | 0 | 1 | 1 | 0 |

Rows 1–3 use the same inputs except for impact (0.700, 0.710, and 0.720). Row 4 uses evidence row 10 with impact changed to 0.770. Each candidate predicts a distinct sequence across the four rows. Thus the labels can distinguish all four candidates. A different sequence would reject all four.
