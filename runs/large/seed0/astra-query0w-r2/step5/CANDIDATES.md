# Candidate rules for step 5

Let `f(x)` be the logit from `model_in.json`. Escalate only when the proposed logit is greater than zero. Let `m = maintenance_window` and `u = users_affected`.

## Evidence

The current model disagrees with 15 of the 32 current labels. Each disagreement changes escalate to suppress. All 15 cases have `m = 1` and `u < 0.5`. Their largest `u` is approximately 0.47659. The two maintenance cases with `u > 0.5` already have zero logits. All cases with `m = 0` keep their current labels.

## 1. Region override — preferred

Set the logit to zero when `m = 1` and `u < 0.5`. Otherwise, keep `f(x)`.

This rule suppresses alerts during maintenance when the normalized `users_affected` value is below 0.5. It preserves the current model outside that region, including maintenance alerts with `u >= 0.5`.

## 2. Output shift

Use `f(x) - 50*m`.

This rule applies a fixed maintenance penalty. The largest current maintenance logit in the evidence is approximately 43.79647, so the penalty suppresses every supplied maintenance case. An unseen maintenance alert with `f(x) > 50` still escalates. The value 50 is a proposed round constant, not an identified parameter.

## 3. Input re-interpretation

When `m = 1`, create `T(x)` by setting `impact`, `urgency`, and `error_rate` to zero, and `confidence` to one. Keep all other features unchanged. Use `f(T(x))`. When `m = 0`, use `f(x)`.

This rule treats maintenance alerts as expected events with no reported impact, urgency, or errors. It changes four input values rather than directly setting the decision. All transformed inputs remain within the permitted ranges. Its decisions can still depend on the unchanged features.

## Verification and selection

Direct forward passes confirm that each candidate matches all 32 current labels. No training, optimization, or parameter search was used. The earlier evidence files contain historical labels; later corrections can override them. Each candidate uses the supplied model, which contains the earlier edits, and leaves its logit unchanged outside the candidate's stated maintenance region. This check does not establish agreement with every historical label after all corrections.

Choose candidate 1. The concentration of changed cases below `users_affected = 0.5` supports a maintenance exception for larger incidents. This candidate also changes a smaller region than the other two. The evidence does not establish the exact threshold, the equality case, or whether suppression should extend to all maintenance alerts. The threshold 0.5 and strict inequality are proposed assumptions.

No model was edited. No query file was created because the query budget is zero.
