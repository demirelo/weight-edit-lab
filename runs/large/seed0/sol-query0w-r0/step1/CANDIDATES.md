# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Each rule escalates only when its resulting logit is greater than zero. Row numbers below exclude the CSV header.

## A. Ignore anger

**Kind: Input re-interpretation.** Evaluate `f(x)` after setting `tone_anger = 0`. Keep every other input unchanged. Apply this rule to all inputs.

Interpretation: The alert decision must not depend on the reporter's anger.

## B. Increase the threshold for limited reach

**Kind: Output shift.** If `users_affected <= 0.8`, use `f(x) - 50`. Otherwise, use `f(x)`.

Interpretation: Alerts with limited reach require a larger original logit. This candidate preserves the anger input and changes the output threshold within a feature region.

## C. Allow anger only with high impact and urgency

**Kind: Interaction.** Keep the original `tone_anger` only when both `impact >= 0.8` and `urgency >= 0.65`. Otherwise, set `tone_anger = 0`. Evaluate `f` on the resulting inputs.

Interpretation: The effect of anger depends on impact and urgency. Unlike A, this rule retains the original anger response when both conditions hold.

## Evidence check and selection

Forward passes confirm that each candidate matches all 32 labels. Each suppresses the original model's positive decisions on rows 1–16 and preserves the labels on rows 17–32. No training, fitting, or weight changes were used.

**Best-supported candidate: A.** Removing anger alone explains every changed label and preserves every other supplied label. It requires no feature thresholds or output offset. B and C also match the evidence, but their additional thresholds are not established by these examples.

The examples do not identify a unique rule or establish behavior on unseen inputs. No query rows are permitted in this phase. The model remains unchanged.
