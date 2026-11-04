# Candidate rules

Let f(x) be the unchanged logit from model_in.json. Let x0 equal x with tone_anger set to zero. Each candidate escalates only when its proposed logit is greater than zero.

## A. Input re-interpretation: ignore anger

Use gA(x) = f(x0) for every input. Anger does not affect escalation. This is the leading hypothesis: it explains all 16 changed labels and all 16 unchanged labels without a new threshold.

## B. Output shift: raise the escalation threshold

Use gB(x) = f(x) - 49.25 for every input. This constant is a candidate, not an identified value. The largest original logit among negative examples is 49.229383; the smallest among positive examples is 49.302516. Thus a shift of 49.25 matches every label, although the evidence leaves only a narrow margin.

## C. Interaction: impact and urgency enable the anger effect

If impact >= 0.90 AND urgency >= 0.60, use gC(x) = f(x). Otherwise, use gC(x) = f(x0). Thus the effect of anger depends on two other features. This differs from A by retaining anger for alerts with high impact and urgency. The thresholds are hypotheses; the evidence does not establish them.

All three candidates match all 32 supplied labels. These checks used forward passes only. No training, fitting, or model edits were performed.

## Query design

Rows 1-4 separate rule kinds. Rows 5-7 change one feature from row 1: impact, urgency, and anger, respectively. Row 8 changes only anger from row 2. These paired queries test the interaction and the effect of anger.

The table gives candidate predictions, not oracle answers. Row numbers exclude the CSV header.

| Query row | A | B | C |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 0 | 1 | 0 |
| 4 | 0 | 1 | 1 |
| 5 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 |
| 8 | 1 | 1 | 1 |
