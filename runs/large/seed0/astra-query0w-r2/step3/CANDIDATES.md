# Step 3 candidate rules

Let `z(x)` be the unchanged logit from `model_in.json`. Let `e` be
`error_rate`, and let `t` be `tier_critical`. Escalate when the candidate
logit is greater than zero. Define `R` as `t = 1 and e > 0.7`.

1. **Region override — selected.** Force escalation inside `R`. Keep the
   current decision outside `R`. A decision-level formula is
   `escalate = R or (z(x) > 0)`. This rule makes high error rates sufficient
   for escalation on a critical tier, regardless of the other inputs.

2. **Output shift.** Use `z_new(x) = z(x) + 100 * indicator(R)`.
   Keep the current logit outside `R`. Inside `R`, add a fixed bonus.
   Unlike candidate 1, this rule still suppresses an alert if its current
   logit is at most `-100`.

3. **Interaction.** Use
   `z_new(x) = z(x) + 2000 * ReLU(e + t - 1.7)`.
   For a critical tier, each unit of error rate above `0.7` adds 2000
   logit units. For a noncritical tier, the added term is zero throughout
   the valid input range. This rule gives error rate an additional effect
   that depends on tier. Unlike candidate 2, its bonus starts at zero and
   increases with error rate. A negative current logit can still suppress
   an alert just above the threshold.

## Evidence and selection

All three candidates match all 32 labels in `evidence.csv`: they change
rows 1–16 from suppress to escalate and preserve rows 17–32. Row numbers
exclude the header. The changed rows have current logits from about
`-85.939` to `-4.560`; all have a critical tier and error rate above `0.7`.
The constants in candidates 2 and 3 are explicit hypotheses, checked by
forward passes. They were not trained or optimized.

Candidate 1 has the strongest support. It explains the changes with one
simple condition and needs no bonus magnitude. The evidence does not
uniquely establish the threshold: for a strict `e > threshold` override,
every threshold from `0.5321322640797269` inclusive to
`0.7388152401588863` exclusive gives the same supplied step-3 labels.
The selected value `0.7` is a hypothesis. No example fixes the label at
exactly `0.7`; these candidates preserve the current decision there.

The candidates are distinct decision rules. On 10,000 unlabelled valid
inputs generated with NumPy seed 31, candidates 1/2, 1/3, and 2/3 differed
on 1, 56, and 55 decisions, respectively. These checks establish distinct
predictions, not correctness on unknown labels.

## Earlier evidence

The unchanged model matches all 32 labels in each earlier evidence file.
Each candidate preserves all step-2 labels and 30 of 32 step-1 labels.
Step-1 rows 4 and 18 become escalations because they fall inside `R`.
These are explicit proposed step-3 overrides of historical labels, as
permitted by TASK.md; the files contain labels from their respective
steps, not a common final target. All three candidates retain the current
model outside `R` and add no dependence on `tone_anger`.

No model edit or query file was made in this phase.
