# Candidate rules for step 4

Let `f(x)` be the unchanged `model_in.json` logit, `u = urgency`, and
`c = confidence`. Each rule escalates when its resulting logit is greater
than zero. Row numbers below exclude the CSV header.

## 1. Conditional urgency rescaling — input re-interpretation

When `c < 0.4`, evaluate `f` with `urgency = 2u`. Otherwise, evaluate `f(x)`.
Keep every other input unchanged. Do not clip the modified urgency: its
internal value can reach 2, although the supplied input remains in [0, 1].

This rule gives urgency more weight when confidence is low, through the
current model's existing feature interactions.

## 2. Conditional urgency bonus — interaction

Use `f(x) + 80u` when `c < 0.4`; otherwise, use `f(x)`.

Confidence controls an additional linear effect of urgency. This differs
from candidate 1 because it adds a fixed slope after the current model,
instead of changing hidden activations.

## 3. Two fixed bonuses — output shift

Add the following bonus to `f(x)`:

| Raw input region | Bonus |
| --- | ---: |
| `c < 0.4` and `u < 0.3` | 10 |
| `c < 0.4` and `u >= 0.3` | 60 |
| `c >= 0.4` | 0 |

This rule assigns a constant bonus within each region. It differs from
candidate 2, whose bonus varies continuously with urgency within the
low-confidence region.

## Verification

I checked each stated rule with forward passes on all 32 labelled examples.
I did not train, fit, or edit the model.

| Candidate | Matching labels | Smallest signed logit margin |
| --- | ---: | ---: |
| 1. Conditional urgency rescaling | 32/32 | 1.355870 |
| 2. Conditional urgency bonus | 32/32 | 0.518897 |
| 3. Two fixed bonuses | 32/32 | 1.651385 |

The signed margin is the logit for label 1 and its negative for label 0.
Each candidate changes rows 1–16 from suppress to escalate and preserves
the current decisions on rows 17–32. These checks establish agreement on
the examples only; they do not establish the intended rule elsewhere.

## Selected candidate

**Candidate 1 is best supported.** One conditional rescaling explains all
labels and retains the current model's response to other features. It
requires fewer separate constants than the two-region output shift.
Candidate 2 remains a plausible alternative.

The evidence does not determine the exact confidence threshold. All changed
rows have confidence at most 0.369; the unchanged rows with higher
confidence start at 0.454. For these candidate formulas, any threshold
strictly above 0.369 and at most 0.454 selects the same example rows.
The value 0.4 is a simple hypothesis, not a confirmed boundary. The labels
also do not uniquely determine the scaling factor, bonus slope, or bonus
levels. The larger sample margin of candidate 3 does not establish that it
is the intended rule.

No query rows were requested. No model edit was made.
