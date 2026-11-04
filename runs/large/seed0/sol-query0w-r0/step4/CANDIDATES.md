# Candidate rules for step 4

Let `F(x)` be the unchanged `model_in.json` logit. Escalate when the candidate logit is greater than zero. All thresholds below are hypotheses, not confirmed boundaries.

## 1. Region override — provisional choice

Force escalation inside either of these two boxes:

- `confidence < 0.5`, `urgency > 0.2`, and `impact > 0.45`.
- `confidence < 0.5` and `urgency > 0.6`.

Set the logit to `1` inside this union. Use `F(x)` elsewhere.

Interpretation: low confidence must not block an alert with sufficient impact or urgency. The minimum urgency excludes high-impact alerts with very low urgency.

## 2. Output shift

Add `1` to `F(x)` when all these conditions hold:

- `confidence < 0.5`.
- `urgency > 0.2`.
- `impact + urgency > 0.8`.
- `error_rate > 0.1` or `tier_critical == 1`.

Use `F(x)` elsewhere.

Interpretation: combined severity earns a bonus when confidence is low and error rate or service tier supplies additional evidence. This rule uses a severity sum and a diagnostic condition, so its decision region differs from candidate 1.

## 3. Input re-interpretation

When `confidence < 0.5`, `urgency > 0.2`, and either `impact > 0.2` or `urgency > 0.6`, replace the impact input with:

`impact_effective = min(1, impact + 0.5)`.

Keep all other inputs unchanged. Evaluate the unchanged model on these inputs. Use `F(x)` outside this condition.

Interpretation: low confidence causes the model to underestimate impact. The remaining network still determines escalation. For example, evidence row 31 enters this condition but remains suppressed after the input change.

## Evidence and selection

Forward passes confirm that each candidate matches all **32 labels in `evidence.csv`**, including all 16 changed decisions and all 16 unchanged decisions. No training, fitting, or weight edits were used.

**Choose candidate 1 provisionally.** It explains the changed examples with two simple boxes. Candidates 2 and 3 require extra assumptions about diagnostic evidence or impact adjustment. The examples do not establish any candidate as the unique rule. They also do not establish the exact thresholds or boundary inclusivity.

Historical evidence needs separate treatment: the unchanged input model already disagrees with step 1 rows 9, 11, and 16, and step 2 rows 22, 25, and 32. Therefore, current-example agreement does not certify preservation of every earlier correction. Historical labels can also change under a later correction.

No model file or query file was written.
