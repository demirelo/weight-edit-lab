# Candidate rules for step 5

Let `f(x)` be the unchanged logit from `model_in.json`. Escalate only when the candidate logit is greater than zero. Let `m = maintenance_window`, `u = users_affected`, and `v = urgency`.

Define region `B` as:

`m = 1 AND (u < 0.5 OR v < 0.6)`.

This region is the union of two boxes of raw feature values. All other features remain unrestricted. These thresholds are hypotheses, not confirmed boundaries.

## 1. Region override — selected provisionally

Suppress every alert in `B`: use logit zero there. Use `f(x)` everywhere else.

This rule treats maintenance as a reason to suppress alerts when either user exposure or urgency is low. It overrides earlier escalation rules only inside `B`.

## 2. Output shift

Use `f(x) - 64` inside `B`. Use `f(x)` everywhere else.

This rule applies a fixed maintenance penalty. Unlike candidate 1, it permits escalation inside `B` when the original logit exceeds 64. The largest original logit among the supplied examples in `B` is approximately 60.967. The value 64 is a proposed round constant; the labels do not establish its true value.

## 3. Interaction

Use:

`f(x) - m * (4096 * max(0, 0.5 - u) + max(0, 0.6 - v))`.

This rule makes the effect of user exposure and urgency depend on maintenance status. Outside maintenance, it preserves the original logit. During maintenance, the penalty increases continuously as either feature falls below its threshold. The constants are explicit hypotheses, chosen by arithmetic reasoning and checked by forward passes; no training or fitting procedure was used.

Unlike candidate 2, the penalty varies with the inputs. Near a threshold, this candidate can retain an escalation that candidates 1 and 2 suppress.

## Evidence and selection

Forward-pass checks confirm that each candidate matches all 32 labels in `evidence.csv`, using the strict `logit > 0` decision rule.

Candidate 1 has the strongest support among these three proposals. It requires no penalty magnitude. Rows 1–16 all have maintenance enabled and user exposure below 0.5. All have label zero; 14 currently have positive logits. Rows 24 and 31 retain escalation during maintenance with higher user exposure and urgency.

Row 18 prevents selection of the simpler rule “suppress only when maintenance is enabled and user exposure is below 0.5.” Its user exposure is approximately 0.697458, urgency is 0.326090, and current logit is 0.177016, but its label is zero. The low-urgency branch covers this case. One case provides weak support for that entire branch. The evidence does not establish a unique intended rule or exact thresholds.

## Earlier evidence

The historical files contain labels at earlier stages, not additional step-5 labels. The current model matches all 32 step-4 labels. It differs from 7 step-1 labels, 1 step-2 label, and 1 step-3 label. Those differences already exist before these proposals. As TASK.md permits later corrections to override earlier labels, historical labels must be interpreted in stage order, not imposed simultaneously.

Each proposal starts from the complete current model and preserves its logit outside `B`. Earlier behavior inside `B` is subject to the proposed new correction. Matching the current examples does not prove that every earlier intended rule is preserved everywhere.

No model edit or query file was made. No query labels are available in this phase.
