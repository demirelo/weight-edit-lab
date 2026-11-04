# Candidate rules for step 4

Let `F(x)` be the logit from `model_in.json`. Escalate when the proposed logit is greater than zero. Each candidate below matches all 32 labels in `evidence.csv`, including all 16 changes from the current decision. These checks used forward passes only. No weights were changed.

The earlier evidence files contain labels from their respective steps. Later corrections can override those labels, as TASK.md states. The candidates use the current model as their starting point; historical labels do not form one combined set of current labels.

## 1. Input re-interpretation — selected

Apply the current model with `urgency` multiplied by **1.8**. Keep every other input unchanged:

`G(x) = F(x with urgency = 1.8 * urgency)`.

Do not clamp the modified urgency to 1. The factor applies across the full input domain, with no confidence condition.

**Check:** 32/32 labels match. The smallest signed logit margin is approximately 0.355. Multiplication by 2 fails on row 25; multiplication by 1.8 preserves that negative label.

## 2. Output shift

Add a bonus to the current logit when `confidence < 0.4`:

- Add 60 when `urgency > 0.3`.
- Add 15 when `0.2 < urgency <= 0.3`.
- Add 0 otherwise.

When `confidence >= 0.4`, add 0. Use `G(x) = F(x) + bonus`.

**Check:** 32/32 labels match. Row 25 stays negative with the smaller bonus. Row 31 stays negative even with the larger bonus.

## 3. Region override

Force escalation inside either of these boxes of raw input values:

- Box A: `confidence < 0.4` and `urgency > 0.6`.
- Box B: `confidence < 0.4`, `impact > 0.45`, and `urgency > 0.2`.

All other features are unrestricted within their stated domains. Set `G(x) = 1` inside either box. Use `G(x) = F(x)` outside both boxes.

**Check:** 32/32 labels match. Both boxes exclude the unchanged negative cases.

## Selection and uncertainty

Select candidate 1. It explains every new label with one scale factor and needs no extra thresholds or override boxes. It retains the current model's computation on the modified input.

The evidence does not establish a unique rule. For example, applying the same urgency scale only when `confidence < 0.4` also matches all 32 labels. The exact factor, confidence condition, and behavior between examples remain uncertain. With queries disabled, candidate 1 is the simplest supported choice, not a proven recovery of the intended rule.
