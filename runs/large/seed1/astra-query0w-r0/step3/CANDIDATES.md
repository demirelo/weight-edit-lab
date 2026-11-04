# Candidate rules

Let `L(x)` be the unchanged `model_in.json` logit. Escalate when the candidate logit is greater than zero. Let `t = tier_critical` and `e = error_rate`.

Each candidate matches all 32 labels in `evidence.csv`. Forward checks also confirm that each matches all 64 labels in `evidence_step1.csv` and `evidence_step2.csv`. No weights were changed or fitted.

1. **Region override — selected.** Force escalation when `t = 1` and `e >= 0.700`. Otherwise, use the current decision. Equivalently, use logit `1` inside this region and `L(x)` outside it. All other features are unrestricted.

2. **Output shift.** Use `L(x) + 120` when `t = 1` and `e >= 0.700`; otherwise use `L(x)`. The bonus exceeds the largest negative logit magnitude among the changed examples, approximately `116.861`. Unlike candidate 1, this rule can still suppress cases with a sufficiently negative current logit. A constructed-input check found an affected case with current logit approximately `-122.059`, which this candidate suppresses.

3. **Interaction.** Use `L(x) + 8192 * t * max(e - 0.690, 0)`. Critical tier activates an increasing error-rate bonus. Noncritical cases retain their current logits. The hand-chosen coefficient gives a bonus of `81.92` at `e = 0.700`, which covers both examples at that value. Forward checks confirm all remaining labels. Unlike candidates 1 and 2, this rule can change decisions below `0.700`.

## Selection and limits

Candidate 1 has the strongest support. All 16 changed examples have critical tier and error rate at least `0.700`, despite large differences in their other features and current logits. Noncritical cases and critical cases with lower error rates retain their current decisions. The changed example at exactly `0.700` supports an inclusive boundary.

The labels do not establish a unique rule or exact threshold. The bonus sizes and candidate 3's lower boundary are hypotheses. Matching prior examples does not prove preservation of earlier corrections on unseen inputs.

No model edit or query file was made in this phase.
