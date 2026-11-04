# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Each candidate escalates exactly when its proposed logit is greater than zero. Unspecified inputs retain their original values.

## 1. Input re-interpretation: ignore anger

Set `tone_anger = 0` before evaluating the current model:

`g1(x) = f(x with tone_anger = 0)`.

This rule removes anger as an escalation signal for all inputs.

## 2. Output shift: apply a context-dependent penalty

Subtract 65 from the current logit if `maintenance_window = 1` or `confidence < 0.2`. Otherwise, subtract 40:

`g2(x) = f(x) - (65 if maintenance_window = 1 or confidence < 0.2 else 40)`.

This rule reduces escalation generally and applies a larger penalty during maintenance or when confidence is low. The constants are hand-chosen hypotheses, not established policy thresholds.

## 3. Interaction: let confidence and tier control anger

Retain `tone_anger` only when `tier_critical = 1` and `confidence >= 0.8`. Otherwise, set it to zero:

`g3(x) = f(x)` in that joint region; elsewhere, `g3(x) = f(x with tone_anger = 0)`.

This rule permits anger to affect the decision only for critical-tier alerts with high confidence. It differs from candidate 1 outside the supplied examples.

## Evidence check and selection

Direct forward passes confirm that each candidate matches all 32 labels. Each suppresses the 16 originally positive examples in rows 1–16 and preserves the labels in rows 17–32. No training or parameter fitting was used.

**Select candidate 1.** It explains every correction through one input change, without extra thresholds or conditions. Its smallest signed margin is approximately 0.00364, on positive example 29, so the strict `logit > 0` decision rule matters.

The labels do not uniquely identify the intended rule. Candidate 2 requires several additional assumptions. Candidate 3 assumes an exception that these labels cannot establish. Candidate 1 is the simplest supported hypothesis, not a proven rule for unseen inputs.
