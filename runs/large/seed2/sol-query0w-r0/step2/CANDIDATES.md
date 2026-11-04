# Candidate rules for step 2

Let `f(x)` be the logit from `model_in.json`, `e = region_eu`, and
`u = urgency`. Each candidate escalates if its resulting logit is strictly
greater than zero. Each candidate keeps the current logit when `e = 0`.

## 1. Output shift: constant EU bonus

Use `g(x) = f(x) + 20e`.

EU alerts receive a logit bonus of 20. Other alerts keep their current logit.
This changes all 16 changed examples to escalate and keeps all 16 current
near-miss labels. It also matches all 32 labels in `evidence_step1.csv`.

## 2. Input re-interpretation: increase EU impact

Evaluate the current model with `impact' = impact + 0.2e`. Keep every other
input unchanged: `g(x) = f(x with impact replaced by impact')`.

Do not clip the internal transformed value. It can reach 1.2; the raw input
still stays in its specified range. This candidate changes how the model
interprets impact for EU alerts. It matches all 32 current labels and all
32 earlier labels.

## 3. Interaction: urgency controls the EU bonus

Use `g(x) = f(x) + 20e(1 + u)`.

The EU bonus increases from 20 to 40 as urgency increases from zero to one.
Thus, urgency has an additional effect only for EU alerts. This candidate
matches all 32 current labels and all 32 earlier labels.

## Selected candidate

Select candidate 1. All 16 changed examples have `region_eu = 1` and current
logits between approximately -17.7921 and -0.3153. A constant EU bonus is a
simple explanation that keeps every supplied near-miss label.

The evidence does not establish the exact bonus or a unique rule. Across both
evidence files, any constant EU bonus `b` with
`17.7920966481 < b <= 35.3341587994` matches every label. The value 20 is a
simple choice within that interval. Candidates 2 and 3 remain possible.

Verification used forward passes only. No model weights were changed. No
query inputs were requested or written.
