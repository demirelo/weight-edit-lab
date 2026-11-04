# Candidate rules for step 4

Let `F(x)` be the current model logit. Escalate when the candidate logit is strictly positive. Each rule below matches all 32 labels in `evidence.csv`: it changes rows 1–16 to escalation and preserves rows 17–32.

## 1. Double urgency at low confidence

**Kind: Input re-interpretation.**

When `confidence < 0.4`, replace `urgency` with `2 * urgency` and evaluate the current model on that modified input. Otherwise, use `F(x)`. Keep all other features unchanged. Do not cap the modified urgency at 1; the internal value can reach 2.

## 2. Add a bonus when an urgency-adjusted score is positive

**Kind: Output shift.**

The current network has the form:

`F(x) = max(B(x), error_rate - 0.7 - (1 - tier_critical))`.

Here, `B(x)` is the dense network score plus `20 * region_eu`. To compute it, take units 0–63 from the second hidden layer, apply their existing weights into unit 0 of the third layer, add that unit's bias, and add `20 * region_eu`. Unit indices start at zero.

Use `F(x) + 2` when both `confidence < 0.4` and `B(x) + 100 * urgency > 0`. Otherwise, use `F(x)`.

This rule uses a fixed urgency contribution to select the bonus region. It does not recompute hidden activations with modified urgency.

## 3. Escalate in four low-confidence regions

**Kind: Region override.**

Force escalation when `confidence < 0.4` and at least one condition holds:

- `impact > 0.9`.
- `urgency > 0.65`.
- `impact > 0.7` and `urgency > 0.3`.
- `users_affected > 0.7` and `urgency > 0.5`.

These conditions define a union of four boxes in raw feature space. Other features can take any allowed value. Outside these boxes, use `F(x)`.

## Selected candidate

**Select candidate 1.** It explains all labels with one condition and one feature transformation. Candidate 2 needs an additional score approximation. Candidate 3 needs four separate regions. Capping the doubled urgency at 1 causes candidate 1 to fail rows 3, 6, 9, 14, 15, and 16.

The evidence does not uniquely identify the rule or the confidence threshold. Treat `0.4` and the strict inequality as proposed choices. No query labels are available in this phase.

## Checks and limits

Forward passes confirm 32/32 matching labels for each candidate. On 10,000 additional inputs from NumPy's `default_rng(4)`, with valid binary features, candidates 1/2, 1/3, and 2/3 disagree on 249, 421, and 474 decisions, respectively. These inputs have no known labels; this check establishes that the rules differ, not which rule is correct.

No training, parameter fitting, or model edits were performed. These checks do not establish that a future edit preserves every earlier correction. No query file or output model was written.
