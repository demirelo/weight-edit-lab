# Candidate rules for step 4

Let `f(x)` be the unchanged logit from `model_in.json`, `u` be
`urgency`, and `c` be `confidence`. Each candidate escalates when its
resulting logit is strictly greater than zero. Each uses the current model,
including its earlier corrections.

## 1. Input re-interpretation — double urgency at low confidence

If `c < 0.4`, evaluate `f(x')`, where `x'` equals `x` except that
`urgency = 2*u`. Otherwise, evaluate `f(x)`.

Do not cap the transformed urgency at 1. The raw input remains in its
specified range; the internal transformed value can reach 2.

## 2. Output shift — add a constant within each urgency region

If `c >= 0.4`, use `f(x)`. If `c < 0.4`, add the following bonus to `f(x)`:

| Raw urgency | Logit bonus |
| --- | ---: |
| `u < 0.5` | 30 |
| `0.5 <= u < 0.75` | 45 |
| `u >= 0.75` | 70 |

This rule changes the final logit without changing the model inputs.

## 3. Interaction — confidence controls an extra urgency effect

Use `f(x) + 81*u*I(c < 0.4)`, where `I` equals 1 when its condition
is true and 0 otherwise.

Below the confidence threshold, urgency has an additional linear effect
on the logit. At or above the threshold, this extra effect is zero.
Unlike candidate 2, the bonus varies continuously with urgency within
each confidence region. Unlike candidate 1, it does not change the
activations inside the current model.

## Evidence check and selection

Forward passes gave these results. No model weights were changed or fitted.

| Candidate | Current evidence | Step 1 evidence | Step 2 evidence | Step 3 evidence |
| --- | ---: | ---: | ---: | ---: |
| 1: Input re-interpretation | 32/32 | 32/32 | 32/32 | 32/32 |
| 2: Output shift | 32/32 | 32/32 | 32/32 | 32/32 |
| 3: Interaction | 32/32 | 32/32 | 32/32 | 32/32 |

**Select candidate 1.** It explains all available labels with one input
scaling rule. The unchanged model matches only 17/32 current labels;
all 15 disagreements have confidence below 0.4. Doubling urgency resolves
all 15 and preserves the other 17 labels. Capping the doubled urgency
at 1 fails current rows 5, 7, 9, 10, and 15.

The labels do not uniquely establish the rule, the exact confidence
threshold, or behavior on unseen inputs. Candidate 1 is the preferred
hypothesis. Agreement with earlier evidence does not prove preservation
of every earlier correction over the full input domain.

No queries were requested. This phase leaves the model unchanged.
