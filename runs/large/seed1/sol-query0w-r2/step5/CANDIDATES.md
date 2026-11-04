# Candidate rules for step 5

Let `f(x)` be the logit from `model_in.json`. Escalate when the candidate logit is greater than zero. Row numbers below exclude the CSV header.

Define two disjoint regions:

- **A:** `maintenance_window = 1` and `users_affected < 0.5`.
- **B:** `maintenance_window = 0`, `users_affected < 0.5`, `tier_critical = 0`, `impact < 0.5`, and `urgency < 0.5`.

## Candidate 1: Output shift

Use `f(x) - 768` in A, `f(x) - 8` in B, and `f(x)` elsewhere.

This rule adds a large maintenance penalty for alerts with low user exposure. It adds a smaller penalty for noncritical alerts with low impact and urgency outside maintenance. These constants are hypotheses, not measured policy values.

## Candidate 2: Region override — selected

Force suppression in A or B. Keep the existing model decision elsewhere. A candidate logit is `min(f(x), 0)` inside these regions and `f(x)` elsewhere.

This rule treats maintenance with low user exposure as a suppression condition. It also suppresses noncritical alerts when user exposure, impact, and urgency are all low.

## Candidate 3: Input re-interpretation

Apply the following condition:

`users_affected < 0.6` and either `maintenance_window = 1` or (`tier_critical = 0`, `impact < 0.5`, and `urgency < 0.5`).

When the condition holds, set `impact`, `urgency`, `tier_critical`, and `region_eu` to zero in a copy of the input. Evaluate the unchanged model on that copy. Otherwise, evaluate the original input.

This rule removes severity and routing signals for alerts with limited user exposure. It uses the wider threshold `0.6`, which the current examples also permit.

## Evidence and selection

Forward passes confirm that each candidate matches **32 of 32** labels in `evidence.csv`. Each changes the existing model decision on rows 1–11, 13, and 15–17. Each preserves the other current example labels. No model weights were changed, and no training or parameter-fitting loop was used.

The candidates imply different decisions beyond the examples:

- Candidate 1 can retain escalation inside A. For example, copy evidence row 1 and set `urgency = 1` and `region_eu = 1`. Its existing logit is approximately `787.216`; Candidate 1 escalates, while Candidate 2 suppresses.
- Candidate 3 can suppress outside A and B. Set all features to zero, then set `users_affected = 0.55`, `error_rate = 1`, `tier_critical = 1`, and `maintenance_window = 1`. Candidates 1 and 2 retain escalation at approximately `612.302`; Candidate 3 suppresses at approximately `-72.354`.

**Select Candidate 2.** The repeated maintenance examples support a suppression condition, including cases with a large critical-tier bonus. This candidate needs no penalty magnitude and preserves the current model outside its stated regions.

The selection remains uncertain. Row 17 has maintenance off and changes from an existing logit of approximately `5.323` to label 0. Thus, a maintenance-only override does not explain every current label. Region B is a tentative explanation for that row. The examples do not establish its exact boundaries, the user threshold, or strict versus inclusive comparisons.

Historical CSV labels describe earlier steps and can be overridden by later corrections. The supplied model already disagrees with 8, 3, 2, and 0 labels in steps 1–4, respectively. The 32/32 result above applies to the current evidence; it does not prove preservation of every earlier rule on unseen inputs.
