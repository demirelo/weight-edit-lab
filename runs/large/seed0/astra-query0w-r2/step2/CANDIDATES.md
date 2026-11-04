# Candidate rules

Let `f(x)` be the current model logit. Escalate exactly when the candidate logit is greater than zero. Let `E = region_eu`, `u = urgency`, and `c = confidence`.

The earlier correction appears to remove the effect of `tone_anger`. All its first-layer weights are zero, and the current model matches all 32 earlier labels. Each candidate preserves this independence for every input.

## A. Output shift

Add 20 to `f(x)` when `E = 1` and `u <= 0.9`. Otherwise, use `f(x)`.

This rule gives EU alerts a fixed bonus below an urgency threshold. The threshold is a hypothesis, not an identified boundary. An unconditional EU bonus of 20 would change earlier labels 6 and 8; this condition preserves them.

## B. Input re-interpretation — selected

Use the current model with urgency replaced by `min(1, u + 0.2 * E)`. Keep every other input unchanged.

This rule increases EU urgency by 0.2 and caps it at 1. Non-EU inputs retain their exact current logits. The rule preserves the earlier correction because the current model ignores `tone_anger`.

## C. Interaction

Use `f(x) + 18 + 3*c` when `E = 1` and `u <= 0.9`. Otherwise, use `f(x)`.

This rule makes the additional effect of confidence depend on EU status and urgency. Within the specified region, each unit increase in confidence adds 3 to the logit beyond its current effect. Outside that region, confidence retains its current effect. This differs from A's constant bonus and B's change to the model input.

## Verification and selection

Forward passes gave these results. Row numbers above exclude the CSV header.

| Candidate | Current labels matched | Earlier labels matched | Smallest current signed margin |
| --- | --- | --- | --- |
| A | 32/32 | 32/32 | 3.827532 |
| B | 32/32 | 32/32 | 0.404675 |
| C | 32/32 | 32/32 | 1.973424 |

The signed margin is the logit for a positive label and its negative for a zero label.

Select B. It explains all available labels with one conditional input change and a standard input cap. A and C need an extra urgency condition to preserve the earlier labels. The examples do not prove B or determine its exact offset; selection rests on simplicity and full agreement with the available labels. No training, parameter fitting, or model edit was performed. No query file was created.
