# Candidate rules

Let `L(x)` be the unchanged `model_in.json` logit, `E = region_eu`, and `T = tier_critical`. Each candidate escalates if its adjusted logit is strictly greater than zero. Each preserves the input model outside the EU.

1. **A: EU increase of 18.** Use `L(x) + 18*E`.
2. **B: EU increase of 20.** Use `L(x) + 20*E`.
3. **C: EU increase of 25.** Use `L(x) + 25*E`.
4. **D: EU increase with a critical-tier addition.** Use `L(x) + E*(20 + 5*T)`.

Each candidate matches all 32 labels in `evidence.csv`. Rows 1–16 change from 0 to 1. Rows 17–32 retain their labels. These are hypotheses; the evidence does not establish one rule.

The changed EU examples have logits from -17.884140 to -1.164971. The closest EU negative example has logit -27.265382. This leaves room for different increases and a tier condition. The first-layer weights for `tone_anger` are all zero. Each candidate preserves that independence.

## Query design

Rows 1–4 test noncritical alerts. Rows 5–8 test critical alerts. All other features remain fixed. Every row separates at least two candidates. The complete label sequences distinguish all four candidates. The paired points also test different possible thresholds within the gaps.

| Query row | Input logit | A | B | C | D |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | -19.508106 | 0 | 1 | 1 | 1 |
| 2 | -18.209272 | 0 | 1 | 1 | 1 |
| 3 | -23.387841 | 0 | 0 | 1 | 0 |
| 4 | -20.806939 | 0 | 0 | 1 | 0 |
| 5 | -19.402227 | 0 | 1 | 1 | 1 |
| 6 | -18.786893 | 0 | 1 | 1 | 1 |
| 7 | -23.709571 | 0 | 0 | 1 | 1 |
| 8 | -21.248232 | 0 | 0 | 1 | 1 |

Only forward passes were used to check the hypotheses and query inputs. No model weights were changed.
